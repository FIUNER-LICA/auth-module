"""
Internationalization (i18n) manager.
"""

from collections.abc import Callable

from .translations import BACKEND_TRANSLATIONS


class I18nManager:
    """
    Generic translation manager for handling localized strings in python applications.
    """

    def __init__(
        self,
        locale: str | Callable[[], str] = 'es',
        default_translations: dict[str, dict[str, str]] | None = None,
        custom_translations: dict[str, dict[str, str]] | None = None
    ):
        """
        Initializes the I18nManager.

        Args:
            locale (str | Callable[[], str]): Language string (e.g. 'es') or callback returning the locale code.
            default_translations (dict[str, dict[str, str]] | None): Fallback translations to load.
            custom_translations (dict[str, dict[str, str]] | None): Customer-supplied dictionary overrides.
        """
        self._locale = locale

        # Load default translations
        if default_translations is None:
            default_translations = BACKEND_TRANSLATIONS

        self.translations: dict[str, dict[str, str]] = {}
        for lang, keys in default_translations.items():
            self.translations[lang] = dict(keys)

        if custom_translations:
            self.load_custom_translations(custom_translations)

    def get_locale(self) -> str:
        """
        Resolves the active locale code.

        Returns:
            str: The active locale code.
        """
        if callable(self._locale):
            return self._locale()
        return self._locale

    def set_locale(self, locale: str | Callable[[], str]) -> None:
        """
        Updates the active locale or localization callback.

        Args:
            locale: Language string or callback.
        """
        self._locale = locale

    def load_custom_translations(self, custom: dict[str, dict[str, str]]) -> None:
        """
        Merges custom dictionary translations into the active dictionary.

        Args:
            custom (dict[str, dict[str, str]]): A dictionary of custom translations to merge.
        """
        for lang, keys in custom.items():
            if lang not in self.translations:
                self.translations[lang] = {}
            self.translations[lang].update(keys)

    def translate(self, key: str, **kwargs) -> str:
        """
        Translates a key into the active locale.
        If the key is not found, it falls back to Spanish ('es') or returns the key itself.

        Args:
            key: The translation key.
            kwargs: Parameters to format inside the translation string.
        """
        locale = self.get_locale()

        msg = self.translations.get(locale, {}).get(key)

        if msg is None:
            # Fallback to Spanish translation
            msg = self.translations.get('es', {}).get(key, key)

        return msg.format(**kwargs)

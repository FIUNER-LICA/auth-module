{% extends 'base.html' %}

{% block content %}
<h2>Verificación de correo</h2>
<p>{{ message }}</p>
<a href="{{ url_for('auth.login') }}">Ir al login</a>
{% endblock %}

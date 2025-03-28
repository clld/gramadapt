<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "languages" %>
<%block name="title">${_('Language')} ${ctx.name}</%block>

<h2>${_('Language')} ${ctx.name}</h2>

${ctx.name} is ${'focus' if ctx.focus else 'neighbour'} language in the contact set(s)
<ul>
    % for cs in ctx.contactsets:
    <li>${h.link(request, cs)}</li>
    % endfor
</ul>

<%def name="sidebar()">
    ${util.language_meta()}
</%def>

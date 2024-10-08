<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! from clld_markdown_plugin import markdown %>
<%! active_menu_item = "rationales" %>
<%block name="title">${_('Rationale')} ${ctx.name}</%block>

<h2>${_('Rationale')} ${ctx.name}</h2>


% if ctx.description:
${markdown(req, ctx.markdown)|n}
% endif

<h3>Questions</h3>
% if ctx.domain_questions:
${request.get_datatable('parameters', h.models.Parameter, rationale=ctx).render()}
% else:
<ul>
    % for q in ctx.questions:
    <li>${h.link(req, q)}</li>
    % endfor
</ul>
% endif


<%def name="sidebar()">
<%util:well title="Author">
<p>${h.linked_contributors(req, ctx)}</p>
</%util:well>
<%util:well title="Sources">
${util.sources_list(sorted([ref.source for ref in ctx.references], key=lambda s: s.name))}
</%util:well>
</%def>

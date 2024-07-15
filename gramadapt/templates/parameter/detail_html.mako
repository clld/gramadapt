<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>


% if ctx.datatype not in {'Comment', 'Value'}:
<div class="span4" style="float: right; margin-top: 1em;">
    <%util:well title="Values">
        <table class="table table-condensed">
            % for de in ctx.domain:
            <tr>
                <td>${h.map_marker_img(req, de)}</td>
                <td>${de.name}</td>
                <td>${de.description}</td>
                <td class="right">${len(de.values)}</td>
            </tr>
            % endfor
        </table>
    </%util:well>
</div>
% endif

<h2>${_('Parameter')} ${ctx.name}</h2>
<dl class="dl-horizontal">
    <dt>Rationale:</dt><dd>${h.link(req, ctx.rationale)}</dd>
    <dt>Domain:</dt><dd>${ctx.dom}</dd>
    <dt>Datatype:</dt><dd>${ctx.datatype}</dd>
</dl>
% if ctx.description:
<p>${ctx.description}</p>
% endif

<div style="clear: both"/>
% if ctx.datatype not in {'Comment'}:
${request.map.render()}
% endif

% if ctx.datatype == 'Comment':
<%util:table items="${ctx.valuesets}" args="item">
    <%def name="head()">
        <th>Contact set</th>
        <th>Answer</th>
    </%def>
    <td>${h.link(request, item.contribution)}</td>
    <td>
        <span class="alignment">${item.values[0].name}</span>
    </td>
</%util:table>
% else:
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
% endif
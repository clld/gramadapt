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
    <dt>Domain:</dt><dd>${h.link(req, ctx.domain_rationale, label=ctx.dom)}</dd>
    % if ctx.rationale:
    <dt>Rationale:</dt><dd>${h.link(req, ctx.rationale)}</dd>
    % endif
    <dt>Datatype:</dt><dd>${ctx.datatype}</dd>
</dl>
% if ctx.description:
<p>${ctx.description}</p>
% endif

<div style="clear: both"/>
% if ctx.datatype not in {'Comment', 'Value'}:
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
% elif ctx.datatype == 'Value':
<table style="width: 100%" class="table table-condensed">
    <tr>
        <th style="width: 70%">
            <div style="float: left">${ctx.minimum}</div>
            <div style="float: right">${ctx.maximum}</div>
        </th>
        <th style="width: 10%"> </th>
        <th style="width: 20%"> </th>
    </tr>
    % for vs, s, e in ctx.iter_ranges():
    <tr>
        <td>
            % if s > 0:
                <div style="float: left; width: ${s}%; background-color: white; color: white">x</div>
            % endif
            <div title="${vs.values[0].name + ('\n' if vs.jsondata['comment'] else '') + vs.jsondata['comment']}" style="color: ${vs.contribution.color_rgba(0.0)}; overflow: visible; float: left; width: ${e}%; background-color: ${vs.contribution.color_rgba(0.2)}; border: 1px solid ${vs.contribution.color};">
                x
            </div>
        </td>
        <td>${vs.values[0].name}</td>
        <td>${h.link(req, vs.contribution)}</td>
    </tr>
    % endfor
</table>
% else:
${request.get_datatable('values', h.models.Value, parameter=ctx).render()}
% endif
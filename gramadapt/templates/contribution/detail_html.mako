<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${_('Contribution')} ${ctx.name}</h2>

<p>
    by <strong>${ctx.authors}</strong>
</p>

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#timeframe" data-toggle="tab">Timeframe</a></li>
        <li><a href="#answers" data-toggle="tab">Answers</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="timeframe" class="tab-pane active">
            % for v in ctx.timeframe_comments():
            <h4>${h.link(req, v.valueset.parameter.timeframe, label=v.valueset.parameter.name)}</h4>
            <p>
                ${v.name}
            </p>
                % if v.description:
            <p><em>${v.description}</em></p>
                % endif
            % endfor
        </div>
        <div id="answers" class="tab-pane">
            <% dt = request.get_datatable('values', h.models.Value, contribution=ctx) %>
            ${dt.render()}
        </div>
    </div>
    <script>
$(document).ready(function() {
    if (location.hash !== '') {
        $('a[href="#' + location.hash.substr(2) + '"]').tab('show');
    }
    return $('a[data-toggle="tab"]').on('shown', function(e) {
        return location.hash = 't' + $(e.target).attr('href').substr(1);
    });
});
    </script>
</div>

<%def name="sidebar()">
<%util:well title="Author">
<p>${h.linked_contributors(req, ctx)}</p>
</%util:well>
<%util:well>
${request.map.render()}
</%util:well>
</%def>

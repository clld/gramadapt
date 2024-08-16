<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${_('Contributions')}</%block>

<h2>${_('Contributions')}</h2>

<p>
    Each contact set is unique in terms of the timeframe they respond for. We urge researchers who use this dataset
    to read the comments in the "Timeframe" tab carefully for each set, to get a sense of the heterogeneity of
    timeframes represented in each set, as well as the whole dataset.
</p>

${request.get_map('languages').render()}

<div>
    ${ctx.render()}
</div>

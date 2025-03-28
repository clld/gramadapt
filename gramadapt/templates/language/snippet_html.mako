<%inherit file="../snippet.mako"/>
<%namespace name="util" file="../util.mako"/>

% if request.params.get('parameter'):
    ## called for the info windows on parameter maps
    ##<% valueset = h.DBSession.query(h.models.ValueSet).filter(h.models.ValueSet.parameter_pk == int(request.params['parameter'])).filter(h.models.ValueSet.language_pk == ctx.pk).first() %>
    <h3>${h.link(request, ctx)}</h3>

    % for valueset in h.DBSession.query(h.models.ValueSet).filter(h.models.ValueSet.language_pk == ctx.pk).filter(h.models.ValueSet.parameter_pk == int(request.params.get('parameter'))):
        <h4>${h.link(request, valueset)}</h4>
        <ul class='unstyled'>
            % for value in valueset.values:
            <li>
                ${h.map_marker_img(request, value)}
                ${h.link(request, valueset, label=str(value))}
                ${h.format_frequency(request, value)}
            </li>
            % endfor
        </ul>
    % endfor
% else:
<h3>${h.link(request, ctx)}</h3>
    % if ctx.description:
        <p>${ctx.description}</p>
    % endif
${h.format_coordinates(ctx)}
% endif

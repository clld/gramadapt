<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Sidebar</h3>
        <p>
            Content
        </p>
    </div>
</%def>

<h2>${ctx.name}</h2>

<p class="lead">
    ${ctx.description}
</p>

<table width="100%">
    <tr>
        <td style="width: 20%; padding-right: 20px;">
            <a href="https://erc.europa.eu/homepage">
                <img src="${req.static_url('gramadapt:static/ERC_Logo.jpg')}">
            </a>
        </td>
        <td width="60%">
    This dataset has been created in the project
            <a href="https://www.helsinki.fi/en/researchgroups/linguistic-adaptation">Linguistic Adaptation: Typological and Sociolinguistic Perspectives to Language Variation</a>.
    The project has received funding from the European Research Council (ERC) under the
            European Union's Horizon 2020 research and innovation programme (<a href="https://doi.org/10.3030/805371">grant agreement No 805371; PI Kaius Sinnemäki</a>),
    and has been hosted at the University of Helsinki.
        </td>
        <td style="width: 20%; padding-right: 20px;">
            <a href="https://www.helsinki.fi/en">
                <img src="${req.static_url('gramadapt:static/University_of_Helsinki_Logo.jpg')}">
            </a>
        </td>
</table>

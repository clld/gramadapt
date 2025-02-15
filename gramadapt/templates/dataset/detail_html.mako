<%inherit file="../home_comp.mako"/>

<%def name="sidebar()">
    <div class="well">
        <h3>Cite as</h3>
        <p>
            Eri Kashima, Francesca Di Garbo, Oona Raatikainen, Kaius Sinnemäki, Ricardo Napoleão de Souza,
            Anu Hyvönen, Kayleigh Karinen, Rosnátaly Avelino, Sacha Beck, Anna Berge, Ana Blanco, Ross Bowden,
            Nicolás Brid, Joseph Brincat, María Belén Carpio, Alexander Cobbinah, Paola Cúneo, Anne-Maria Fehn,
            Saloumeh Gholami, Arun Ghosh, Hannah Gibson, Elizabeth Hall, Katja Hannß, Hannah Haynie, Jerry Jacka,
            Matias Jenny, Richard Kowalik, Sonal Kulkarni-Joshi, Maarten Mous, Marcela Mendoza, Cristina Messineo,
            Francesca Moro, Hank Nater, Michelle Ocasio, Bruno Olsson, Ana María Ospina Bozzi, Agustina Paredes,
            Admire Phiri, Nicolas Quint, Erika Sandman, Dineke Schokkin, Ruth Singer, Ellen Smith-Dennis,
            Lameen Souag, Yunus Sulistyono, Yvonne Treis, Matthias Urban, Jill Vaughan, Deginet Wotango Doyiso,
            Georg Ziegelmeyer, Veronika Zikmundová,
            Robert Forkel. (2025). GramAdapt Crosslinguistic Social Contact Dataset (v1.1) [Data set]. Zenodo.
            <a href="https://doi.org/10.5281/zenodo.14872294">https://doi.org/10.5281/zenodo.14872294</a>
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

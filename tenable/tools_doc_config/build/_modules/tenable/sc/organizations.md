
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.organizations &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/custom.css" />
    
    <script data-url_root="../../../" id="documentation_options" src="../../../_static/documentation_options.js"></script>
    <script src="../../../_static/jquery.js"></script>
    <script src="../../../_static/underscore.js"></script>
    <script src="../../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../../genindex.md" />
    <link rel="search" title="Search" href="../../../search.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" accesskey="U">tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.organizations</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.organizations</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Organizations</span>
<span class="sd">=============</span>

<span class="sd">The following methods allow for interaction with the Tenable.sc</span>
<span class="sd">:sc-api:`Organization &lt;Organization.html&gt;` API. These items are typically seen</span>
<span class="sd">under the **Organization** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.organizations``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: OrganizationAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.sc.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>


<div class="viewcode-block" id="OrganizationAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI">[docs]</a><span class="k">class</span> <span class="nc">OrganizationAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Organization document constructor</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Validate the the name attribute is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the description is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;address&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the address field is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;address&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;address&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;city&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the city is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;city&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;city&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;state&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the state is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;state&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;state&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;country&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the country is a streing value.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;country&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;country&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;phone&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the phone is a string value.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;phone&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;phone&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;lce_ids&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that the lce_ids is a list of integers and transform them</span>
            <span class="c1"># into a list of dictionaries with id attributes.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;lces&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lce:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                          <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lce_ids&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;lce_ids&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;lce_ids&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;zone_selection&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate that zone_selection is a string value of one of the</span>
            <span class="c1"># expected types and store it in the camelCase equiv.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;zoneSelection&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;zone_selection&#39;</span><span class="p">,</span>
                                              <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;zone_selection&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                    <span class="s1">&#39;auto_only&#39;</span><span class="p">,</span> <span class="s1">&#39;locked&#39;</span><span class="p">,</span> <span class="s1">&#39;selectable&#39;</span><span class="p">,</span> <span class="s1">&#39;selectable+auto&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;selectable+auto_restricted&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;zone_selection&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;restricted_ips&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># ensure that restricted_ips is a list of items and return it as a</span>
            <span class="c1"># comma-seperated string in the camelCase variant of the param.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;restrictedIPs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;restricted_ips&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;restricted_ips&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">))</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;restricted_ips&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;repos&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of numeric ids for repos into a list of</span>
            <span class="c1"># dictionaries with the id attribute.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;repositories&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">r</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                                  <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repos&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;repos&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;repos&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;pub_sites&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of numeric ids for pub_sites into a list of</span>
            <span class="c1"># dictionaries with the id attribute.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s2">&quot;pubSites&quot;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;site:id&#39;</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                              <span class="k">for</span> <span class="n">p</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;pub_sites&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;pub_sites&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s2">&quot;pub_sites&quot;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;ldap_ids&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of numeric ids for ldap_ids into a list of</span>
            <span class="c1"># dictionaries with the id attribute.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ldaps&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ldap:id&#39;</span><span class="p">,</span> <span class="n">p</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                           <span class="k">for</span> <span class="n">p</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ldap_ids&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ldap_ids&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ldap_ids&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;nessus_managers&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of numeric ids for nessus managers into a list of</span>
            <span class="c1"># dictionaries with the id attribute.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessusManagers&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;nessus_manager:id&#39;</span><span class="p">,</span> <span class="n">n</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                                    <span class="k">for</span> <span class="n">n</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;nessus_managers&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessus_managers&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessus_managers&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;info_links&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the info_links</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ipInfoLinks&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;link:name&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">),</span>
                <span class="s1">&#39;link&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;link:link&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="nb">str</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;info_links&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;info_links&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;info_links&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;vuln_score_low&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vulnScoreLow&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vuln_score_low&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_low&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_low&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;vuln_score_medium&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vulnScoreMedium&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vuln_score_medium&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_medium&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_medium&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;vuln_score_high&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vulnScoreHigh&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vuln_score_high&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_high&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_high&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;vuln_score_critical&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vulnScoreCritical&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;vuln_score_critical&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_critical&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;vuln_score_critical&#39;</span><span class="p">]</span>

        <span class="k">return</span> <span class="n">kwargs</span>

<div class="viewcode-block" id="OrganizationAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Create a new organization</span>

<span class="sd">        :sc-api:`SC Organization Create &lt;Organization.html#organization_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str): The name for organization.</span>
<span class="sd">            info_links (list, optional):</span>
<span class="sd">                A list of custom analysis links provided to users within the</span>
<span class="sd">                host vulnerability details when analyzing data outside of</span>
<span class="sd">                SecurityCenter is desired.  Links shall be described in a tuple</span>
<span class="sd">                format with ``(name, link)`` format.  For example:</span>
<span class="sd">                ``(&#39;SANS&#39;, &#39;https://isc.sans.edu/ipinfo.html?ip=%IP%&#39;)``</span>
<span class="sd">            lce_ids (list, optional):</span>
<span class="sd">                What Log Correlation Engines (if any) should this organization</span>
<span class="sd">                be allowed to access?  If left unspecified no LCE engined will</span>
<span class="sd">                be granted to this organization.</span>
<span class="sd">            ldap_ids (list, optional):</span>
<span class="sd">                What ldap server configuration ids should be used with this</span>
<span class="sd">                organization?</span>
<span class="sd">            nessus_managers (list, optional):</span>
<span class="sd">                Nessus Manager scanner for Nessus Agent scan imports.</span>
<span class="sd">            pub_sites (list, optional):</span>
<span class="sd">                A list of publishing site ids to associate this organization.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                A list of Repository ids to associate to this organization.</span>
<span class="sd">            restricted_ips (list, optional):</span>
<span class="sd">                A list of IP addresses, CIDRs, and/or IP ranges that should</span>
<span class="sd">                never be scanned.</span>
<span class="sd">            vuln_score_low (int):</span>
<span class="sd">                The vulnerability weighting to apply to low criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 1)</span>
<span class="sd">            vuln_score_medium (int):</span>
<span class="sd">                The vulnerability weighting to apply to medium criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 3)</span>
<span class="sd">            vuln_score_high (int):</span>
<span class="sd">                The vulnerability weighting to apply to high criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 10)</span>
<span class="sd">            vuln_score_critical (int):</span>
<span class="sd">                The vulnerability weighting to apply to critical criticality</span>
<span class="sd">                vulnerabilities for scoring purposes.(Default: 40)</span>
<span class="sd">            zone_selection (str):</span>
<span class="sd">                What type of scan zone selection should be performed?</span>
<span class="sd">                Available selection types are as follows: ``auto_only``,</span>
<span class="sd">                ``locked``, ``selectable+auto``,</span>
<span class="sd">                ``selectable+auto_restricted``.</span>
<span class="sd">                If left unspecified, the default is ``auto_only``.</span>
<span class="sd">            zones (list, optional):</span>
<span class="sd">                When ``zone_selection`` is not ``auto_only``, this field</span>
<span class="sd">                must be filled with list of ids from available scan zone(s).</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The organization resource record for the newly created Org.</span>

<span class="sd">        Examples:</span>

<span class="sd">            Creating a new organization with automatic scan zone selection:</span>

<span class="sd">            &gt;&gt;&gt; org = sc.organization.create(&#39;Sample Organization&#39;)</span>

<span class="sd">            Creating a new organization with custom analysis links:</span>

<span class="sd">            &gt;&gt;&gt; org = sc.organization.create(</span>
<span class="sd">            ...     &#39;Sample Organization&#39;,</span>
<span class="sd">            ...     info_links=[</span>
<span class="sd">            ...         (&#39;SANS&#39;, &#39;https://isc.sans.edu/ipinfo.html?ip=%IP%&#39;)</span>
<span class="sd">            ... ])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;zone_selection&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;zone_selection&#39;</span><span class="p">,</span> <span class="s1">&#39;auto_only&#39;</span><span class="p">)</span>
        <span class="n">kwargs</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;organization&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves a list of organizations.</span>

<span class="sd">        :sc-api:`SC organization List &lt;Organization.html#OrganizationRESTReference-/organization&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For</span>
<span class="sd">                details on what fields are available, please refer to the</span>
<span class="sd">                details on the request within the organization list API doc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of organization definitions.</span>

<span class="sd">        Examples:</span>

<span class="sd">            Retrieve all of all of the organizations:</span>

<span class="sd">            &gt;&gt;&gt; repos = sc.organizations.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for the specified organization.</span>

<span class="sd">        :sc-api:`SC Organization Details &lt;Organization.html#organization_id_GET&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            organization_id (int): The numeric id of the organization.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned. For details</span>
<span class="sd">                on what fields are available, please refer to the details on</span>
<span class="sd">                the request within the organization details API doc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The organization resource record.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; org = sc.organization.details(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span>
                <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">]</span>
            <span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;organization_id&#39;</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates an existing organization</span>

<span class="sd">        :sc-api:`SC Organization Edit &lt;Organization.html#organization_id_PATCH&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            organization_id: The numeric id of the organization.</span>
<span class="sd">            info_links (list, optional):</span>
<span class="sd">                A list of custom analysis links provided to users within the</span>
<span class="sd">                host vulnerability details when analyzing data outside of</span>
<span class="sd">                SecurityCenter is desired.</span>
<span class="sd">            lce_ids (list, optional):</span>
<span class="sd">                What Log Correlation Engines (if any) should this organization</span>
<span class="sd">                be allowed to access?  If left unspecified no LCE engined will</span>
<span class="sd">                be granted to this organization.</span>
<span class="sd">            ldap_ids (list, optional):</span>
<span class="sd">                What ldap server configuration ids should be used with this</span>
<span class="sd">                organization?</span>
<span class="sd">            name (str, optional): The name for organization.</span>
<span class="sd">            nessus_managers (list, optional):</span>
<span class="sd">                Nessus Manager scanner for Nessus Agent scan imports.</span>
<span class="sd">            pub_sites (list, optional):</span>
<span class="sd">                A list of publishing site ids to associate this organization.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                A list of Repository ids to associate to this organization.</span>
<span class="sd">            restricted_ips (list, optional):</span>
<span class="sd">                A list of IP addresses, CIDRs, and/or IP ranges that should</span>
<span class="sd">                never be scanned.</span>
<span class="sd">            vuln_score_low (int):</span>
<span class="sd">                The vulnerability weighting to apply to low criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 1)</span>
<span class="sd">            vuln_score_medium (int):</span>
<span class="sd">                The vulnerability weighting to apply to medium criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 3)</span>
<span class="sd">            vuln_score_high (int):</span>
<span class="sd">                The vulnerability weighting to apply to high criticality</span>
<span class="sd">                vulnerabilities for scoring purposes. (Default: 10)</span>
<span class="sd">            vuln_score_critical (int):</span>
<span class="sd">                The vulnerability weighting to apply to critical criticality</span>
<span class="sd">                vulnerabilities for scoring purposes.(Default: 40)</span>
<span class="sd">            zone_selection (str):</span>
<span class="sd">                What type of scan zone selection should be performed?</span>
<span class="sd">                Available selection types are as follows: ``auto_only``,</span>
<span class="sd">                ``locked``, ``selectable+auto``, ``selectable+auto_restricted``.</span>
<span class="sd">                If left unspecified, the default is ``auto_only``.</span>
<span class="sd">            zones (list, optional):</span>
<span class="sd">                When ``zone_selection`` is not ``auto_only``, this field</span>
<span class="sd">                must be filled with list of ids from available scan zone(s).</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The updated organization resource record.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; sc.organization.edit(1, name=&#39;New Name&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kwargs</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;organization_id&#39;</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Remove the specified organization from Tenable.sc</span>

<span class="sd">        :sc-api:`SC organization Delete &lt;Organization.html#organization_id_DELETE&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            organization_id (int): The numeric id of the organization to delete.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty response string</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; sc.organization.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;organization_id&#39;</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">))</span>
        <span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.accept_risk_rules"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.accept_risk_rules">[docs]</a>    <span class="k">def</span> <span class="nf">accept_risk_rules</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                          <span class="n">organization_id</span><span class="p">,</span>
                          <span class="n">repos</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span>
                          <span class="n">plugin</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span>
                          <span class="n">port</span><span class="o">=</span><span class="kc">None</span>
                          <span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the accepted risk rules for the organization and optionally</span>
<span class="sd">        will filter based on the parameters specified.</span>

<span class="sd">        :sc-api:`organization: accept-risk-rule</span>
<span class="sd">        &lt;Organization.html#OrganizationRESTReference-/organization/{organization_id}/acceptRiskRule&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            organization_id (int): The organization id.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                A list of repository ids to restrict the search to.</span>
<span class="sd">            plugin (int, optional):</span>
<span class="sd">                A plugin id to restrict the search to.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                A port number to restrict the search to.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of rules that match the request.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; for rule in sc.organizations.accept_risk_rules(1):</span>
<span class="sd">            ...     pprint(rule)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">repos</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;repositoryIDs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
                                                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repos&#39;</span><span class="p">,</span> <span class="n">repos</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">if</span> <span class="n">plugin</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;pluginID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span> <span class="n">plugin</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">port</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">port</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/acceptRiskRule&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;organization_id&#39;</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.recast_risk_rules"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.recast_risk_rules">[docs]</a>    <span class="k">def</span> <span class="nf">recast_risk_rules</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="n">repos</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">plugin</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">port</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the recasted risk rules for the organization and optionally</span>
<span class="sd">        will filter based on the parameters specified.</span>

<span class="sd">        :sc-api:`organization: recast-risk-rule</span>
<span class="sd">        &lt;Organization.html#OrganizationRESTReference-/organization/{organization_id}/recastRiskRule&gt;`  # noqa: E501</span>

<span class="sd">        Args:</span>
<span class="sd">            organization_id (int): The organization id.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                A list of repository ids to restrict the search to.</span>
<span class="sd">            plugin (int, optional):</span>
<span class="sd">                A plugin id to restrict the search to.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                A port number to restrict the search to.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of rules that match the request.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; for rule in sc.organizations.recast_risk_rules(1):</span>
<span class="sd">            ...     pprint(rule)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">repos</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;repositoryIDs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
                                                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repos&#39;</span><span class="p">,</span> <span class="n">repos</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">if</span> <span class="n">plugin</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;pluginID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span> <span class="n">plugin</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">port</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">port</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/recastRiskRule&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;organization_id&#39;</span><span class="p">,</span> <span class="n">organization_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.managers_list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.managers_list">[docs]</a>    <span class="k">def</span> <span class="nf">managers_list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves a list of security managers.</span>

<span class="sd">        :sc-api:`organization-security-manager: list &lt;Organization-Security-Manager.html#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager&gt;`  # noqa: E501,PLC0301</span>

<span class="sd">        Args:</span>
<span class="sd">            org_id: (int):</span>
<span class="sd">                The numeric identifier for the organization.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the organization list API doc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of user definitions.</span>

<span class="sd">        Examples:</span>

<span class="sd">            Retrieve all of the security managers for a given org.:</span>
<span class="sd">            &gt;&gt;&gt; repos = sc.organizations.managers_list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/securityManager&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.manager_create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.manager_create">[docs]</a>    <span class="k">def</span> <span class="nf">manager_create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="n">role</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new security manager for the given org.  For a complete list</span>
<span class="sd">        of parameters that are supported for this call, please refer to</span>
<span class="sd">        :py:meth:`tio.users.create() &lt;UserAPI.create&gt;` for more details.</span>

<span class="sd">        :sc-api:`organization-security-manager: create &lt;Organization-Security-Manager.html#organization_orgID_securityManager_POST&gt;`  # noqa: E501,PLC0301</span>

<span class="sd">        Args:</span>
<span class="sd">            org_id: (int):</span>
<span class="sd">                The numeric identifier for the organization.</span>
<span class="sd">            username (str):</span>
<span class="sd">                The username for the account</span>
<span class="sd">            password (str):</span>
<span class="sd">                The password for the user to create</span>
<span class="sd">            role (int):</span>
<span class="sd">                The role that should be assigned to this user.</span>
<span class="sd">            **kwargs (dict):</span>
<span class="sd">                The keyword args to pass to the user constructor.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created security manager.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; secmngr = sc.organizations.manager_create(1,</span>
<span class="sd">            ...     &#39;username&#39;, &#39;password&#39;, 1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;username&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">username</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;password&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">password</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;role&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">role</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;auth_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auth_type&#39;</span><span class="p">,</span> <span class="s1">&#39;tns&#39;</span><span class="p">)</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;responsibleAssetID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">users</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/securityManager&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.manager_details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.manager_details">[docs]</a>    <span class="k">def</span> <span class="nf">manager_details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details of a specified security manager within a</span>
<span class="sd">        specified organization.</span>

<span class="sd">        :sc-api:`organization-security-manager: details &lt;Organization-Security-Manager.html#OrganizationSecurityManagerRESTReference-/organization/{orgID}/securityManager/{id}&gt;`  # noqa: E501,PLC0301</span>

<span class="sd">        Args:</span>
<span class="sd">            org_id: (int):</span>
<span class="sd">                The numeric identifier for the organization.</span>
<span class="sd">            user_id: (int):</span>
<span class="sd">                The numeric identifier for the user.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the organization list API doc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The user resource record.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; secmngr = sc.organizations.manager_details(1, 1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/securityManager/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">),</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;user_id&#39;</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.manager_edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.manager_edit">[docs]</a>    <span class="k">def</span> <span class="nf">manager_edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits the specified security manager within the specified organization.</span>
<span class="sd">        For details on the supported arguments that may be passed, please refer</span>
<span class="sd">        to :py:meth:`tio.users.edit() &lt;UserAPI.edit&gt;` for more details.</span>

<span class="sd">        :sc-api:`organization-security-manager: edit &lt;Organization-Security-Manager.html#organization_orgID_securityManager_id_PATCH&gt;`  # noqa: E501,PLC0301</span>

<span class="sd">        Args:</span>
<span class="sd">            org_id: (int):</span>
<span class="sd">                The numeric identifier for the organization.</span>
<span class="sd">            user_id: (int):</span>
<span class="sd">                The numeric identifier for the user.</span>
<span class="sd">            **kwargs (dict):</span>
<span class="sd">                The keyword args to pass to the user constructor.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated user record.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; secmngr = sc.organizations.manager_edit(1, 1,</span>
<span class="sd">            ...     username=&#39;updated&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">users</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/securityManager/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">),</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;user_id&#39;</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="p">),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="OrganizationAPI.manager_delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.organizations.OrganizationAPI.manager_delete">[docs]</a>    <span class="k">def</span> <span class="nf">manager_delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="n">migrate_to</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the user specified.</span>

<span class="sd">        :sc-api:`organization-security-manager: delete &lt;Organization-Security-Manager.html#organization_orgID_securityManager_id_DELETE&gt;`  # noqa: E501,PLC0301</span>

<span class="sd">        Args:</span>
<span class="sd">            org_id: (int):</span>
<span class="sd">                The numeric identifier for the organization.</span>
<span class="sd">            user_id: (int):</span>
<span class="sd">                The numeric identifier for the user.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; sc.organizations.manager_delete(1, 1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">migrate_to</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;migrateUserID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;migrate_to&#39;</span><span class="p">,</span> <span class="n">migrate_to</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;organization/</span><span class="si">{}</span><span class="s1">/securityManager/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">),</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;user_id&#39;</span><span class="p">,</span> <span class="n">user_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="p">),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div></div>
</pre></div>

            <div class="clearer"></div>
          </div>
      </div>
      <div class="clearer"></div>
    </div>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" >tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.organizations</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
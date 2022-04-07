<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../genindex.md" />
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.repositories</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.repositories</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Repositories</span>
<span class="sd">============</span>
<span class="sd">The following methods allow for interaction with the Tenable.sc</span>
<span class="sd">:sc-api:`Repository &lt;Repository.html&gt;` API.  These items are typically seen</span>
<span class="sd">under the **Repositories** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.repositories``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: RepositoryAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">semver</span> <span class="kn">import</span> <span class="n">VersionInfo</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="RepositoryAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI">[docs]</a><span class="k">class</span> <span class="nc">RepositoryAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Repository document constructor</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;nessus_sched&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessusSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schedule_constructor</span><span class="p">(</span><span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessus_sched&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessus_sched&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;mobile_sched&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mobileSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schedule_constructor</span><span class="p">(</span><span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mobile_sched&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mobile_sched&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;remote_sched&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remoteSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schedule_constructor</span><span class="p">(</span><span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_sched&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_sched&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Validate the name is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Verify that the description is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;format&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># The data format for the repository.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;format&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;format&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                                               <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;agent&#39;</span><span class="p">,</span> <span class="s1">&#39;IPv4&#39;</span><span class="p">,</span> <span class="s1">&#39;IPv6&#39;</span><span class="p">,</span> <span class="s1">&#39;mobile&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;format&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;repo_type&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># The type of repository</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo_type&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;repo_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                                         <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Local&#39;</span><span class="p">,</span> <span class="s1">&#39;Remote&#39;</span><span class="p">,</span> <span class="s1">&#39;Offline&#39;</span><span class="p">])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;repo_type&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;orgs&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Validate all of the organizational sub-documents.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;organizations&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">o</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                                       <span class="k">for</span> <span class="n">o</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;orgs&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;trending&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Trending should be between 0 and 365.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trendingDays&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;trending&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trending&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">,</span>
                                                 <span class="n">choices</span><span class="o">=</span><span class="nb">list</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="mi">366</span><span class="p">)))</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trending&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;fulltext_search&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># trendWithRaw is the backend paramater name for &quot;Full Text Search&quot;</span>
            <span class="c1"># within the UI.  We will be calling it fulltest_search to more</span>
            <span class="c1"># closely align with what the frontend calls this feature.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trendWithRaw&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fulltext_search&#39;</span><span class="p">,</span>
                                                     <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fulltext_search&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fulltext_search&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;lce_correlation&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># The correlation parameter isn&#39;t well named here, we will call it</span>
            <span class="c1"># out as LCE correlation to specifically note what it is for.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;correlation&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lce_id&#39;</span><span class="p">,</span> <span class="n">l</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                                     <span class="k">for</span> <span class="n">l</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lce_correlation&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;lce_correlation&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;lce_correlation&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;allowed_ips&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Using valid IPs here instead of ipRange to again more closely</span>
            <span class="c1"># align to the frontend and to more explicitly call out the</span>
            <span class="c1"># function of this paramater</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ipRange&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ip&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                          <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;allowed_ips&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;allowed_ips&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;allowed_ips&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;remote_ip&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remoteIP&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;remote_ip&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_ip&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_ip&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;remote_repo&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remoteID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;remote_repo&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_repo&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remote_repo&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;preferences&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Validate that all of the preferences are K:V pairs of strings.</span>
            <span class="k">for</span> <span class="n">key</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preferences&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">):</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preference:</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">key</span><span class="p">),</span> <span class="n">key</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;preference:</span><span class="si">{}</span><span class="s1">:value&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">key</span><span class="p">),</span>
                            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;preferences&#39;</span><span class="p">][</span><span class="n">key</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;mdm_id&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mdm&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;mdm_id&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mdm_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mdm_id&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;scanner_id&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;scanner&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;scanner_id&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;scanner_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;scanner_id&#39;</span><span class="p">]</span>
        <span class="k">return</span> <span class="n">kwargs</span>
    <span class="k">def</span> <span class="nf">_rules_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Accept/Recast Rule Query Creator</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;plugin_id&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Convert the snake_cased variant to the camelCased variant.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;pluginID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;port&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># validate port is a integer</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;orgs&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of organization IDs into the comma-separated</span>
            <span class="c1"># string that the API expects.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;organizationIDs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org:id&#39;</span><span class="p">,</span> <span class="n">o</span><span class="p">,</span> <span class="nb">int</span><span class="p">))</span>
                                              <span class="k">for</span> <span class="n">o</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;orgs&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;fields&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the list of field names into the comma-separated string</span>
            <span class="c1"># that the API expects.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                     <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]])</span>
        <span class="k">return</span> <span class="n">kwargs</span>
<div class="viewcode-block" id="RepositoryAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">repo_type</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves a list of repositories.</span>
<span class="sd">        :sc-api:`repository: list &lt;Repository.htm#repository_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the repository list API doc.</span>
<span class="sd">            repo_type (str, optional):</span>
<span class="sd">                Restrict the response to a specific type of repository.  If not</span>
<span class="sd">                set, then all repository types will be returned.  Allowed types</span>
<span class="sd">                are ``All``, ``Local``, ``Remote``, and ``Offline``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of repository definitions.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Retrieve all of all of the repositories:</span>
<span class="sd">            &gt;&gt;&gt; repos = sc.repositories.list()</span>
<span class="sd">            Retrieve all of the remote repositories:</span>
<span class="sd">            &gt;&gt;&gt; repos = sc.repositories.list(repo_type=&#39;Remote&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">repo_type</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo_type&#39;</span><span class="p">,</span> <span class="n">repo_type</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;All&#39;</span><span class="p">,</span> <span class="s1">&#39;Local&#39;</span><span class="p">,</span> <span class="s1">&#39;Remote&#39;</span><span class="p">,</span> <span class="s1">&#39;Offline&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new repository</span>
<span class="sd">        :sc-api:`repository: create &lt;Repository.html#repository_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str): The name for the respository.</span>
<span class="sd">            allowed_ips (list, optional):</span>
<span class="sd">                Allowed IPs will restrict incoming data being inserted into the</span>
<span class="sd">                repository to only the IPs that exist within the configured</span>
<span class="sd">                CIDR ranges.  Accepts a list of CIDR strings based on the</span>
<span class="sd">                repository format (IPv4 or IPv6).  If left unspecified, then it</span>
<span class="sd">                will default to the CIDR equivalent of &quot;allow all&quot; for that IP</span>
<span class="sd">                version.  IPv4=0.0.0.0/0, IPv6=::/0.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description for the repository.</span>
<span class="sd">            format (str, optional):</span>
<span class="sd">                The format of the repository.  Valid choices are ``agent``,</span>
<span class="sd">                ``IPv4``, ``IPv6``, and ``mobile``.  The default if unspecified</span>
<span class="sd">                is ``IPv4``.</span>
<span class="sd">            fulltext_search (bool, optional):</span>
<span class="sd">                Should full-text searching be enabled?  This option is used for</span>
<span class="sd">                IPv4, IPv6, and agent repository formats and determins whether</span>
<span class="sd">                the plugin output is trended along with the normalized data.  If</span>
<span class="sd">                left unspecified, the default is set to ``False``.</span>
<span class="sd">            lce_correlation (list, optional):</span>
<span class="sd">                What Log Correlation Engines (if any) should correlate against</span>
<span class="sd">                this repository.  A list of configured LCE numeric IDs is</span>
<span class="sd">                supplied.  This option is used on IPv4, IPv6, and agent formats</span>
<span class="sd">                and is defaulted to nothing if left unspecified.</span>
<span class="sd">            nessus_sched (dict, optional):</span>
<span class="sd">                This is the .Nessus file generation schedule for IPv4 and IPv6</span>
<span class="sd">                repository formats.  This option should only be used if there</span>
<span class="sd">                is a need to consume the Repository in a raw Nessus XML format.</span>
<span class="sd">                If left unspecified, it will default to ``{&#39;type&#39;: &#39;never&#39;}``.</span>
<span class="sd">            mobile_sched (dict, optional):</span>
<span class="sd">                When using the mobile repository format, this option will inform</span>
<span class="sd">                Tenable.sc how often to perform the MDM synchronization into the</span>
<span class="sd">                repository.  If left unspecified, it will default to</span>
<span class="sd">                ``{&#39;type&#39;: &#39;never&#39;}``.</span>
<span class="sd">            orgs (list, optional):</span>
<span class="sd">                A list of Organization IDs used to assign the repository to 1 or</span>
<span class="sd">                many organizations.</span>
<span class="sd">            preferences (dict, optional):</span>
<span class="sd">                When using a mobile repository type, this dictionary details</span>
<span class="sd">                the required preferences to inject into the backend scan needed</span>
<span class="sd">                to communicate to the MDM solution.</span>
<span class="sd">            remote_ip (str, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the IP</span>
<span class="sd">                address of the Tenable.sc instance that the repository will be</span>
<span class="sd">                pulled from.</span>
<span class="sd">            remote_repo (int, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the numeric ID</span>
<span class="sd">                of the repository on the remote host that will be pulled.</span>
<span class="sd">            remote_sched (dict, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the schedule</span>
<span class="sd">                dictionary that will inform Tenable.sc how often to synchronize</span>
<span class="sd">                with the downstream Tenable.sc instance.  If left unspecified</span>
<span class="sd">                then we will default to ``{&#39;type&#39;: &#39;never&#39;}``.</span>
<span class="sd">            repo_type (str, optional):</span>
<span class="sd">                What type of repository is this?  Valid choices are ``Local``,</span>
<span class="sd">                ``Remote``, and ``Offline``.  The default if unspecified is</span>
<span class="sd">                ``Local``.</span>
<span class="sd">            scanner_id (int, optional):</span>
<span class="sd">                When using the mobile repository format, we must specify the</span>
<span class="sd">                scanner from which to query the MDM source.</span>
<span class="sd">            trending (int, optional):</span>
<span class="sd">                How many days of trending snapshots should be created for this</span>
<span class="sd">                repository.  This value is only used for IPv4, IPv6, and agent</span>
<span class="sd">                repositories.  If not supplied, the default will be 0.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The repository resource record for the newly created Repo.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Creating a new IPv4 Repository leveraging the defaults:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(name=&#39;Example IPv4&#39;)</span>
<span class="sd">            Creating a new IPv4 Repository with 90 days of trending and linked</span>
<span class="sd">            to the first Organization:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(</span>
<span class="sd">            ...     name=&#39;Example Trending&#39;, trending=90, orgs=[1])</span>
<span class="sd">            Creating an IPv6 repository:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(</span>
<span class="sd">            ...     name=&#39;Example IPv6&#39;, format=&#39;IPv6&#39;)</span>
<span class="sd">            Creating an agent repository:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(</span>
<span class="sd">            ...     name=&#39;Example Agent&#39;, format=&#39;agent&#39;)</span>
<span class="sd">            Creating an MDM repository for ActiveSync that will sync every day</span>
<span class="sd">            at 6am eastern:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(</span>
<span class="sd">            ...     name=&#39;Example ActiveSync&#39;, mdm_id=1, scanner_id=1,</span>
<span class="sd">            ...     format=&#39;mobile&#39;, orgs=[1],</span>
<span class="sd">            ...     mobile_sched={</span>
<span class="sd">            ...         &#39;repeatRule&#39;: &#39;FREQ=DAILY;INTERVAL=1&#39;,</span>
<span class="sd">            ...         &#39;start&#39;: &#39;TZID=America/New_York:20190212T060000&#39;,</span>
<span class="sd">            ...         &#39;type&#39;: &#39;ical&#39;,</span>
<span class="sd">            ...     },</span>
<span class="sd">            ...     preferences={</span>
<span class="sd">            ...         &#39;domain&#39;: &#39;AD_DOMAIN&#39;,</span>
<span class="sd">            ...         &#39;domain_admin&#39;: &#39;DA_ACCOUNT_NAME&#39;,</span>
<span class="sd">            ...         &#39;domain_controller&#39;: &#39;dc1.company.tld&#39;,</span>
<span class="sd">            ...         &#39;password&#39;: &#39;DA_ACCOUNT_PASSWORD&#39;</span>
<span class="sd">            ... })</span>
<span class="sd">            Creating a new repository to remotely sync the downstream Tenable.sc</span>
<span class="sd">            instance&#39;s repository 1 to this host and institute trending for 90</span>
<span class="sd">            days:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.create(</span>
<span class="sd">            ...     name=&#39;Example Remote Repo&#39;,</span>
<span class="sd">            ...     repo_type=&#39;Remote&#39;,</span>
<span class="sd">            ...     remote_ip=&#39;192.168.0.101&#39;,</span>
<span class="sd">            ...     remote_repo=1,</span>
<span class="sd">            ...     trending=90,</span>
<span class="sd">            ...     orgs=[1],</span>
<span class="sd">            ...     remote_sched={</span>
<span class="sd">            ...         &#39;type&#39;: &#39;ical&#39;,</span>
<span class="sd">            ...         &#39;start&#39;: &#39;TZID=America/NewYork:20190212T060000&#39;,</span>
<span class="sd">            ...         &#39;repeatRule&#39;: &#39;FREQ=DAILY;INTERVAL=1&#39;</span>
<span class="sd">            ... })</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kwargs</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">,</span> <span class="s1">&#39;IPv4&#39;</span><span class="p">)</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="s1">&#39;Local&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;IPv4&#39;</span><span class="p">,</span> <span class="s1">&#39;IPv6&#39;</span><span class="p">,</span> <span class="s1">&#39;agent&#39;</span><span class="p">]:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trendingDays&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;trendingDays&#39;</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;trendWithRaw&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;trendWithRaw&#39;</span><span class="p">,</span> <span class="s1">&#39;false&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;IPv4&#39;</span><span class="p">,</span> <span class="s1">&#39;IPv6&#39;</span><span class="p">]:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;nessusSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;nessusSchedule&#39;</span><span class="p">,</span> <span class="p">{</span><span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;never&#39;</span><span class="p">})</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;IPv4&#39;</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ipRange&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;ipRange&#39;</span><span class="p">,</span> <span class="s1">&#39;0.0.0.0/0&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;IPv6&#39;</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;ipRange&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;ipRange&#39;</span><span class="p">,</span> <span class="s1">&#39;::/0&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;dataFormat&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;mobile&#39;</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;mobileSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;mobileSchedule&#39;</span><span class="p">,</span> <span class="p">{</span><span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;never&#39;</span><span class="p">})</span>
        <span class="k">if</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;remote&#39;</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;remoteSchedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;remoteSchedule&#39;</span><span class="p">,</span> <span class="p">{</span><span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;never&#39;</span><span class="p">})</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;repository&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for the specified repository.</span>
<span class="sd">        :sc-api:`repository: details &lt;Repository.html#repository_id_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id of the repository.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the repository details API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The repository resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.details(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Remove the specified repository from Tenable.sc</span>
<span class="sd">        :sc-api:`repository: delete &lt;Repository.html#repository_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id of the repository to delete.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty response string</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.repositories.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates an existing repository</span>
<span class="sd">        :sc-api:`repository: edit &lt;Repository.html#repository_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id of the repository to edit.</span>
<span class="sd">            allowed_ips (list, optional):</span>
<span class="sd">                Allowed IPs will restrict incoming data being inserted into the</span>
<span class="sd">                repository to only the IPs that exist within the configured</span>
<span class="sd">                CIDR ranges.  Accepts a list of CIDR strings based on the</span>
<span class="sd">                repository format (IPv4 or IPv6).</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description for the repository.</span>
<span class="sd">            lce_correlation (list, optional):</span>
<span class="sd">                What Log Correlation Engines (if any) should correlate against</span>
<span class="sd">                this repository.  A list of configured LCE numeric IDs is</span>
<span class="sd">                supplied.  This option is used on IPv4, IPv6, and agent formats.</span>
<span class="sd">            name (str, optional): The name for the repository.</span>
<span class="sd">            nessus_sched (dict, optional):</span>
<span class="sd">                This is the .Nessus file generation schedule for IPv4 and IPv6</span>
<span class="sd">                repository formats.  This option should only be used if there</span>
<span class="sd">                is a need to consume the Repository in a raw Nessus XML format.</span>
<span class="sd">            mobile_sched (dict, optional):</span>
<span class="sd">                When using the mobile repository format, this option will inform</span>
<span class="sd">                Tenable.sc how often to perform the MDM synchronization into the</span>
<span class="sd">                repository.</span>
<span class="sd">            orgs (list, optional):</span>
<span class="sd">                A list of Organization IDs used to assign the repository to 1 or</span>
<span class="sd">                many organizations.</span>
<span class="sd">            preferences (dict, optional):</span>
<span class="sd">                When using a mobile repository type, this dictionary details</span>
<span class="sd">                the required preferences to inject into the backend scan needed</span>
<span class="sd">                to communicate to the MDM solution.</span>
<span class="sd">            remote_ip (str, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the IP</span>
<span class="sd">                address of the Tenable.sc instance that the repository will be</span>
<span class="sd">                pulled from.</span>
<span class="sd">            remote_repo (int, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the numeric ID</span>
<span class="sd">                of the repository on the remote host that will be pulled.</span>
<span class="sd">            remote_sched (dict, optional):</span>
<span class="sd">                When the Remote repository type is used, this is the schedule</span>
<span class="sd">                dictionary that will inform Tenable.sc how often to synchronize</span>
<span class="sd">                with the downstream Tenable.sc instance.</span>
<span class="sd">            scanner_id (int, optional):</span>
<span class="sd">                When using the mobile repository format, we must specify the</span>
<span class="sd">                scanner from which to query the MDM source.</span>
<span class="sd">            trending (int, optional):</span>
<span class="sd">                How many days of trending snapshots should be created for this</span>
<span class="sd">                repository.  This value is only used for IPv4, IPv6, and agent</span>
<span class="sd">                repositories.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The repository resource record for the newly created Repo.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; repo = sc.repositories.edit(1, name=&#39;Example IPv4&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kwargs</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.accept_risk_rules"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.accept_risk_rules">[docs]</a>    <span class="k">def</span> <span class="nf">accept_risk_rules</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the accepted risk rules associated with the specified</span>
<span class="sd">        repository.</span>
<span class="sd">        :sc-api:`repository: accept rules &lt;Repository.html#RepositoryRESTReference-/repository/{id}/acceptRiskRule&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id of the repository.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the repository accept risk rules API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of the accepted risk rules that apply to the repo.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; rules = sc.repositories.accept_risk_rules(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_rules_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/acceptRiskRule&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.recast_risk_rules"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.recast_risk_rules">[docs]</a>    <span class="k">def</span> <span class="nf">recast_risk_rules</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the recast risk rules associated with the specified</span>
<span class="sd">        repository.</span>
<span class="sd">        :sc-api:`repository: recast rules</span>
<span class="sd">        &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/recastRiskRule&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id of the repository.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the repository recast risk rules API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of the recast risk rules that apply to the repo.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; rules = sc.repositories.recast_risk_rules(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_rules_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/recastRiskRule&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.asset_intersections"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.asset_intersections">[docs]</a>    <span class="k">def</span> <span class="nf">asset_intersections</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="n">uuid</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">ip_address</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">dns</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the asset lists that a UUID, DNS address, or IP exists in.</span>
<span class="sd">        :sc-api:`repository: asst intersections</span>
<span class="sd">        &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/assetIntersections&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric identifier of the repository to query.</span>
<span class="sd">            dns (str): The DNS name to query</span>
<span class="sd">            ip_address (str): The IP address to query</span>
<span class="sd">            uuid (str): The UUID to query.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of assets matching the criteria.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; assetlists = sc.repositories.asset_intersection(1,</span>
<span class="sd">            ...     ip=&#39;192.168.0.1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">dns</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;dnsName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;dns&#39;</span><span class="p">,</span> <span class="n">dns</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">ip_address</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;ip&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ip_address&#39;</span><span class="p">,</span> <span class="n">ip_address</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">uuid</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;uuid&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;uuid&#39;</span><span class="p">,</span> <span class="n">uuid</span><span class="p">,</span> <span class="s1">&#39;uuid&#39;</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/assetIntersections&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;assets&#39;</span><span class="p">)</span></div>
<div class="viewcode-block" id="RepositoryAPI.import_repository"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.import_repository">[docs]</a>    <span class="k">def</span> <span class="nf">import_repository</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="n">fobj</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Imports the repository archive for an offline repository.</span>
<span class="sd">        :sc-api:`repository: import &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/import&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id associated to the offline repository.</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file-like object containing the repository archive.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The import response record.</span>
<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;repo.tar.gz&#39;, &#39;rb&#39;) as archive:</span>
<span class="sd">            ...     sc.repositories.import_repository(1, archive)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/import&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;file&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">fobj</span><span class="p">)</span>
        <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.export_repository"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.export_repository">[docs]</a>    <span class="k">def</span> <span class="nf">export_repository</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="n">fobj</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Exports the repository and writes the archive tarball into the file</span>
<span class="sd">        object passed.</span>
<span class="sd">        :sc-api:`repository: export &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/export&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id associated to the repository.</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file-like object for the repository archive.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The export response record.</span>
<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;repo.tar.gz&#39;, &#39;wb&#39;) as archive:</span>
<span class="sd">            ...     sc.repositories.export_repository(1, archive)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/export&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="c1"># Lets stream the file into the file-like object...</span>
        <span class="k">for</span> <span class="n">chunk</span> <span class="ow">in</span> <span class="n">resp</span><span class="o">.</span><span class="n">iter_content</span><span class="p">(</span><span class="n">chunk_size</span><span class="o">=</span><span class="mi">1024</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">chunk</span><span class="p">:</span>
                <span class="n">fobj</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">chunk</span><span class="p">)</span>
        <span class="n">fobj</span><span class="o">.</span><span class="n">seek</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span>
        <span class="n">resp</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">fobj</span></div>
<div class="viewcode-block" id="RepositoryAPI.remote_sync"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.remote_sync">[docs]</a>    <span class="k">def</span> <span class="nf">remote_sync</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Initiates a remote synchronization with a downstream Tenable.sc</span>
<span class="sd">        instance.  This action can only be performed on an offline repository.</span>
<span class="sd">        :sc-api:`repository: sync &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/sync&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id for the remote repository.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The sync response record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.repositories.remote_sync(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/sync&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.mobile_sync"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.mobile_sync">[docs]</a>    <span class="k">def</span> <span class="nf">mobile_sync</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Initiates a MDM synchronization with the configured MDM source on the</span>
<span class="sd">        mobile repository specified.</span>
<span class="sd">        :sc-api:`repository: update mobile data</span>
<span class="sd">        &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/updateMobileData&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id for the mobile repository to run the sync.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The sync response record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.repositories.mobile_sync(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;repository/</span><span class="si">{}</span><span class="s1">/updateMobileData&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.device_info"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.device_info">[docs]</a>    <span class="k">def</span> <span class="nf">device_info</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="n">dns</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">ip_address</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">uuid</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the device information for the requested device on the</span>
<span class="sd">        associated repository.</span>
<span class="sd">        :sc-api:`repository: device info</span>
<span class="sd">        &lt;Repository.html#RepositoryRESTReference-/repository/{repository_id}/deviceInfo&gt;`</span>
<span class="sd">        `repository: ip info &lt;Repository.html#RepositoryRESTReference-/repository/{id}/ipInfo&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            repository_id (int): The numeric id for the repository to query.</span>
<span class="sd">            dns (str): The DNS name to query</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the repository device info API doc.</span>
<span class="sd">            ip_address (str): The IP address to query</span>
<span class="sd">            uuid (str): The UUID to query.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The device resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; host = sc.repositories.device_info(1, ip_address=&#39;192.168.0.1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># We will generally want to query the deviceInfo action, however if we</span>
        <span class="c1"># happen to be on a Tenable.sc instance version that&#39;s less than 5.7, we</span>
        <span class="c1"># have to instead query ipInfo.</span>
        <span class="n">method</span> <span class="o">=</span> <span class="s1">&#39;deviceInfo&#39;</span>
        <span class="k">if</span> <span class="n">VersionInfo</span><span class="o">.</span><span class="n">parse</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">version</span><span class="p">)</span><span class="o">.</span><span class="n">match</span><span class="p">(</span><span class="s1">&#39;&lt;5.7.0&#39;</span><span class="p">):</span>
            <span class="n">method</span> <span class="o">=</span> <span class="s1">&#39;ipInfo&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span>
                <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">]</span>
            <span class="p">)</span>
        <span class="k">if</span> <span class="n">dns</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;dnsName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;dns&#39;</span><span class="p">,</span> <span class="n">dns</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">ip_address</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;ip&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ip_address&#39;</span><span class="p">,</span> <span class="n">ip_address</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">uuid</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;uuid&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;uuid&#39;</span><span class="p">,</span> <span class="n">uuid</span><span class="p">,</span> <span class="s1">&#39;uuid&#39;</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repository_id&#39;</span><span class="p">,</span> <span class="n">repository_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;repository/</span><span class="si">{</span><span class="n">repository_id</span><span class="si">}</span><span class="s1">/</span><span class="si">{</span><span class="n">method</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">,</span>
                             <span class="n">params</span><span class="o">=</span><span class="n">params</span>
                             <span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.remote_authorize"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.remote_authorize">[docs]</a>    <span class="k">def</span> <span class="nf">remote_authorize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">host</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="n">password</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Authorized communication to a downstream Tenable.sc instance with the</span>
<span class="sd">        provided username and password.</span>
<span class="sd">        :sc-api:`repository: authorize &lt;Repository.html#RepositoryRESTReference-/repository/authorize&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            host (str): The downstream Tenable.sc instance ip address.</span>
<span class="sd">            username (str): The username to authenticate with.</span>
<span class="sd">            password (str); The password to authenticate with.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty response object</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.repositories.remote_authorize(</span>
<span class="sd">            ...     &#39;192.168.0.101&#39;, &#39;admin&#39;, &#39;password&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;repository/authorize&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;host&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;host&#39;</span><span class="p">,</span> <span class="n">host</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
            <span class="s1">&#39;username&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">,</span> <span class="n">username</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
            <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;password&#39;</span><span class="p">,</span> <span class="n">password</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="RepositoryAPI.remote_fetch"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.repositories.RepositoryAPI.remote_fetch">[docs]</a>    <span class="k">def</span> <span class="nf">remote_fetch</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">host</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of repositories from the specified downstream</span>
<span class="sd">        Tenable.sc instance.</span>
<span class="sd">        :sc-api:`repository: fetch remote &lt;Repository.html#RepositoryRESTReference-/repository/fetchRemote&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            host (str): The downstream Tenable.sc instance ip address.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of repositories on the downstream Tenable.sc instance.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repository/fetchRemote&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;host&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;host&#39;</span><span class="p">,</span> <span class="n">host</span><span class="p">,</span> <span class="nb">str</span><span class="p">)})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.repositories</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
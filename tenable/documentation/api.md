<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../../genindex.md" />
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.dashboard.api</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.dashboard.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Dashboard</span>
<span class="sd">=========</span>
<span class="sd">Methods described in this section relate to the the dashboard API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.dashboard``.</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: DashboardAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.dashboard.schema</span> <span class="kn">import</span> <span class="n">DashboardSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<div class="viewcode-block" id="DashboardAPI"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI">[docs]</a><span class="k">class</span> <span class="nc">DashboardAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;dashboards&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">DashboardSchema</span><span class="p">()</span>
<div class="viewcode-block" id="DashboardAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieve all dashboard instances.</span>
<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                The list of dashboard objects.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.dashboard.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>
<div class="viewcode-block" id="DashboardAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">order</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Create a new dashboard instance.</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of the new dashboard.</span>
<span class="sd">            order (int):</span>
<span class="sd">                order of the dashboard.</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The created dashboard instance.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.dashboard.create(</span>
<span class="sd">            ...     name=&#39;new_dashboard&#39;,</span>
<span class="sd">            ...     order=10)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
            <span class="s1">&#39;order&#39;</span><span class="p">:</span> <span class="n">order</span>
        <span class="p">}</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>
<div class="viewcode-block" id="DashboardAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specific dashboard instance.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (str):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The details of the dashboard object of specified dashboard_id.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.dashboard.details(dashboard_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div>
<div class="viewcode-block" id="DashboardAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates the dashboard instance based on ``dashboard_id``.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (str):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                The updated name.</span>
<span class="sd">            order (optional, int):</span>
<span class="sd">                The order of the dashboard.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.dashboard.update(</span>
<span class="sd">            ...     dashboard_id=&#39;23&#39;,</span>
<span class="sd">            ...     name=&#39;updated_dashboard_name&#39;,</span>
<span class="sd">            ...     order=1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span>
            <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>
<div class="viewcode-block" id="DashboardAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.dashboard.md#tenable.ad.dashboard.api.DashboardAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Deletes the dashboard instance</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (str):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.dashboard.delete(dashboard_id=&#39;22&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">)</span></div></div>
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
          <a href="../../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.dashboard.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
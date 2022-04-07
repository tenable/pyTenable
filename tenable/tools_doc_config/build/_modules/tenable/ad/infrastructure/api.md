
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.infrastructure.api &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../../../_static/custom.css" />
    
    <script data-url_root="../../../../" id="documentation_options" src="../../../../_static/documentation_options.js"></script>
    <script src="../../../../_static/jquery.js"></script>
    <script src="../../../../_static/underscore.js"></script>
    <script src="../../../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../../../genindex.md" />
    <link rel="search" title="Search" href="../../../../search.md" /> 
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.infrastructure.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.infrastructure.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Infrastructure</span>
<span class="sd">==============</span>

<span class="sd">Methods described in this section relate to the the infrastructure API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.infrastructure``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: InfrastructureAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.infrastructure.schema</span> <span class="kn">import</span> <span class="n">InfrastructureSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>


<div class="viewcode-block" id="InfrastructureAPI"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI">[docs]</a><span class="k">class</span> <span class="nc">InfrastructureAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;infrastructures&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">InfrastructureSchema</span><span class="p">()</span>

<div class="viewcode-block" id="InfrastructureAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of infrastructures.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                List of infrastructure instances.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.infrastructure.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="InfrastructureAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">login</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">password</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new infrastructure instance with inputs of name, username</span>
<span class="sd">        and password.</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The new name for the infrastructure instance.</span>
<span class="sd">            login (str):</span>
<span class="sd">                The login name for the infrastructure instance.</span>
<span class="sd">            password (str):</span>
<span class="sd">                The password for the infrastructure instance.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                Newly created infrastructure instance.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.infrastructure.create(</span>
<span class="sd">            ...     name=&#39;test_user&#39;,</span>
<span class="sd">            ...     login=&#39;test_user@gmail.com&#39;,</span>
<span class="sd">            ...     password=&#39;tenable.ad&#39;))</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
                <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
                <span class="s1">&#39;login&#39;</span><span class="p">:</span> <span class="n">login</span><span class="p">,</span>
                <span class="s1">&#39;password&#39;</span><span class="p">:</span> <span class="n">password</span>
            <span class="p">}))</span>
        <span class="p">]</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="InfrastructureAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Gets the details of particular infrastructure instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (str):</span>
<span class="sd">                The infrastructure instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                Details of particular ``infrastructure_id``.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.infrastructure.details(infrastructure_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">infrastructure_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div>

<div class="viewcode-block" id="InfrastructureAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates the infrastructure of the specific infrastructure instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (str):</span>
<span class="sd">                The infrastructure instance identifier.</span>
<span class="sd">            name (optional, str):</span>
<span class="sd">                New name to be updated.</span>
<span class="sd">            login (optional, str):</span>
<span class="sd">                New login name to be updated.</span>
<span class="sd">            password (optional, str):</span>
<span class="sd">                New password to be updated.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                Updated infrastructure instance.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.infrastructure.update(</span>
<span class="sd">            ...     infrastructure_id=&#39;1&#39;,</span>
<span class="sd">            ...     login=&#39;updated_login@tenable.com&#39;,</span>
<span class="sd">            ...     name=&#39;updated_user&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">infrastructure_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>

<div class="viewcode-block" id="InfrastructureAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.infrastructure.md#tenable.ad.infrastructure.api.InfrastructureAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">infrastructure_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Deletes the particular infrastructure instance.</span>

<span class="sd">        Args:</span>
<span class="sd">            infrastructure_id (str):</span>
<span class="sd">                The infrastructure instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            None:</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.infrastructure.delete(infrastructure_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">infrastructure_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">),</span>
                                 <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.infrastructure.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
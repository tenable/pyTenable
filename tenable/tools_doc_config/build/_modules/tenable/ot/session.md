
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ot.session &#8212; pyTenable  documentation</title>
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
          <li class="nav-item nav-item-1"><a href="../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ot.session</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ot.session</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Tenable.ot</span>
<span class="sd">==========</span>

<span class="sd">This package covers the Tenable.ot interface.</span>

<span class="sd">.. autoclass:: TenableOT</span>
<span class="sd">    :members:</span>


<span class="sd">.. toctree::</span>
<span class="sd">    :hidden:</span>
<span class="sd">    :glob:</span>

<span class="sd">    assets</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">import</span> <span class="nn">warnings</span>
<span class="kn">from</span> <span class="nn">tenable.base.platform</span> <span class="kn">import</span> <span class="n">APIPlatform</span>
<span class="kn">from</span> <span class="nn">tenable.ot.assets</span> <span class="kn">import</span> <span class="n">AssetsAPI</span>


<div class="viewcode-block" id="TenableOT"><a class="viewcode-back" href="../../../tenable.ot.md#tenable.ot.session.TenableOT">[docs]</a><span class="k">class</span> <span class="nc">TenableOT</span><span class="p">(</span><span class="n">APIPlatform</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The Tenable.ot object is the primary interaction point for users to</span>
<span class="sd">    interface with Tenable.io via the pyTenable library.  All of the API</span>
<span class="sd">    endpoint classes that have been written will be grafted onto this class.</span>

<span class="sd">    Args:</span>
<span class="sd">        api_key (str, optional):</span>
<span class="sd">            The user&#39;s API key for Tenable.ot.  If an api key isn&#39;t specified,</span>
<span class="sd">            then the library will attempt to read the environment variable</span>
<span class="sd">            ``TOT_API_KEY`` to acquire the key.</span>
<span class="sd">        url (str, optional):</span>
<span class="sd">            The base URL used to connect to the Tenable.ot application.  If a</span>
<span class="sd">            url isn&#39;t specified, then the library will attempt to read the</span>
<span class="sd">            environment variable ``TOT_URL`` to acquire the URL.</span>

<span class="sd">        **kwargs:</span>
<span class="sd">            arguments passed to :class:`tenable.base.platform.APIPlatform` for</span>
<span class="sd">            connection management.</span>


<span class="sd">    Examples:</span>
<span class="sd">        Basic Example:</span>

<span class="sd">        &gt;&gt;&gt; from tenable.ot import TenableOT</span>
<span class="sd">        &gt;&gt;&gt; ot = TenableOT(secret_key=&#39;SECRET_KEY&#39;,</span>
<span class="sd">        ..                 url=&#39;https://ot.example.com&#39;)</span>

<span class="sd">        Example with proper identification:</span>

<span class="sd">        &gt;&gt;&gt; ot = TenableOT(secret_key=&#39;SECRET_KEY&#39;,</span>
<span class="sd">        ...                url=&#39;https://ot.example.com&#39;,</span>
<span class="sd">        ...                vendor=&#39;Company Name&#39;,</span>
<span class="sd">        ...                product=&#39;My Awesome Widget&#39;,</span>
<span class="sd">        ...                build=&#39;1.0.0&#39;)</span>

<span class="sd">        Example with proper identification leveraging environment variables for</span>
<span class="sd">        the connection parameters:</span>

<span class="sd">        &gt;&gt;&gt; ot = TenableOT(vendor=&#39;Company&#39;, product=&#39;Widget&#39;, build=&#39;1.0.0&#39;)</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">_env_base</span> <span class="o">=</span> <span class="s1">&#39;TOT&#39;</span>
    <span class="n">_ssl_verify</span> <span class="o">=</span> <span class="kc">False</span>
    <span class="n">_conv_json</span> <span class="o">=</span> <span class="kc">True</span>

    <span class="k">def</span> <span class="nf">_session_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>  <span class="c1"># noqa: PLW0221,PLW0613</span>
        <span class="n">msg</span> <span class="o">=</span> <span class="s1">&#39;Session Auth isn</span><span class="se">\&#39;</span><span class="s1">t supported with the Tenable.ot APIs&#39;</span>
        <span class="n">warnings</span><span class="o">.</span><span class="n">warn</span><span class="p">(</span><span class="n">msg</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="n">msg</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">_key_auth</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">api_key</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>  <span class="c1"># noqa: PLW0221,PLW0613</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_session</span><span class="o">.</span><span class="n">headers</span><span class="o">.</span><span class="n">update</span><span class="p">({</span>
            <span class="s1">&#39;X-APIKeys&#39;</span><span class="p">:</span> <span class="sa">f</span><span class="s1">&#39;key=</span><span class="si">{</span><span class="n">api_key</span><span class="si">}</span><span class="s1">&#39;</span>
        <span class="p">})</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_auth_mech</span> <span class="o">=</span> <span class="s1">&#39;keys&#39;</span>

    <span class="k">def</span> <span class="nf">_authenticate</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;_key_auth_dict&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;_key_auth_dict&#39;</span><span class="p">,</span> <span class="p">{</span>
            <span class="s1">&#39;api_key&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;api_key&#39;</span><span class="p">,</span>
                                  <span class="n">os</span><span class="o">.</span><span class="n">getenv</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_env_base</span><span class="si">}</span><span class="s1">_API_KEY&#39;</span><span class="p">)</span>
                                  <span class="p">)</span>
        <span class="p">})</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_authenticate</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

<div class="viewcode-block" id="TenableOT.graphql"><a class="viewcode-back" href="../../../tenable.ot.md#tenable.ot.session.TenableOT.graphql">[docs]</a>    <span class="k">def</span> <span class="nf">graphql</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        GraphQL Endpoint</span>

<span class="sd">        This singular method exposes the GraphQL API to the library.  As all</span>
<span class="sd">        keyword arguments are passed directly to the JSON body, it allows for a</span>
<span class="sd">        freeform interface into the GraphQL API.</span>

<span class="sd">        Args:</span>
<span class="sd">            **kwargs (dict, optional):</span>
<span class="sd">                The key/values that should be passed to the body of the GraphQL</span>
<span class="sd">                request.</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; ot.graphql(</span>
<span class="sd">            ...     variables={&#39;asset&#39;: &#39;b64 id string&#39;},</span>
<span class="sd">            ...     query=\&#39;\&#39;\&#39;</span>
<span class="sd">            ...         query getAssetDetails($asset: ID!) {</span>
<span class="sd">            ...             asset(id: $asset) {</span>
<span class="sd">            ...                 id</span>
<span class="sd">            ...                 type</span>
<span class="sd">            ...                 name</span>
<span class="sd">            ...                 criticality</span>
<span class="sd">            ...                 location</span>
<span class="sd">            ...             }</span>
<span class="sd">            ...         }</span>
<span class="sd">            ... \&#39;\&#39;\&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;graphql&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">kwargs</span><span class="p">)</span></div>

    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">assets</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The interface object for the</span>
<span class="sd">        :doc:`Tenable.ot Assets APIs &lt;assets&gt;`.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">AssetsAPI</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.session</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
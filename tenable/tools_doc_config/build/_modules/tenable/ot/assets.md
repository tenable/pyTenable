
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ot.assets &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.assets</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ot.assets</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Assets</span>
<span class="sd">======</span>

<span class="sd">Methods described in this section relate to the the assets API.</span>
<span class="sd">These methods can be accessed at ``TenableOT.assets``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AssetsAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Optional</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.ot.graphql.assets</span> <span class="kn">import</span> <span class="p">(</span>
    <span class="n">ASSETS_QUERY</span><span class="p">,</span>
    <span class="n">ASSETS_QUERY_OBJECT_NAME</span><span class="p">,</span>
    <span class="n">AssetsSchema</span>
<span class="p">)</span>
<span class="kn">from</span> <span class="nn">tenable.ot.graphql.definitions</span> <span class="kn">import</span> <span class="n">GraphObject</span>
<span class="kn">from</span> <span class="nn">tenable.ot.graphql.iterators</span> <span class="kn">import</span> <span class="n">OTGraphIterator</span>


<div class="viewcode-block" id="AssetsAPI"><a class="viewcode-back" href="../../../tenable.ot.md#tenable.ot.assets.AssetsAPI">[docs]</a><span class="k">class</span> <span class="nc">AssetsAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;assets&#39;</span>

<div class="viewcode-block" id="AssetsAPI.list"><a class="viewcode-back" href="../../../tenable.ot.md#tenable.ot.assets.AssetsAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
             <span class="nb">filter</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">dict</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
             <span class="n">search</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
             <span class="n">sort</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">List</span><span class="p">[</span><span class="nb">dict</span><span class="p">]]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
             <span class="n">start_at</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
             <span class="n">limit</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">int</span><span class="p">]</span> <span class="o">=</span> <span class="mi">200</span><span class="p">,</span>
             <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves a list of assets via the GraphQL API.</span>

<span class="sd">        Args:</span>
<span class="sd">            filter(dict, optional):</span>
<span class="sd">                A document as defined by Tenable.ot online documentation.</span>
<span class="sd">            search(str, optional):</span>
<span class="sd">                A search string to further limit the response.</span>
<span class="sd">            sort(list[dict], optional):</span>
<span class="sd">                A list of order documents, each of which must contain both the</span>
<span class="sd">                ``field`` and ``direction`` keys and may also contain the</span>
<span class="sd">                optional ``function`` key. Default sort is by descending id</span>
<span class="sd">                order. Please refer to Tenable.ot online documentation for more</span>
<span class="sd">                information.</span>
<span class="sd">            start_at(str, optional):</span>
<span class="sd">                The cursor to start the scan from (the default is an empty</span>
<span class="sd">                cursor).</span>
<span class="sd">            limit(int, optional):</span>
<span class="sd">                Max number of objects that get retrieved per page (the default</span>
<span class="sd">                is 200).</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`OTGraphIterator`:</span>
<span class="sd">                An iterator object that will handle pagination of the data.</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt;     for asset in tot.assets.list(limit=500):</span>
<span class="sd">                        print(asset)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">sort</span><span class="p">:</span>
            <span class="n">sort</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;field&#39;</span><span class="p">:</span> <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="s1">&#39;direction&#39;</span><span class="p">:</span> <span class="s1">&#39;DescNullLast&#39;</span><span class="p">}]</span>

        <span class="n">query_variables</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;search&#39;</span><span class="p">:</span> <span class="n">search</span><span class="p">,</span>
            <span class="s1">&#39;sort&#39;</span><span class="p">:</span> <span class="n">sort</span><span class="p">,</span>
            <span class="s1">&#39;startAt&#39;</span><span class="p">:</span> <span class="n">start_at</span><span class="p">,</span>
            <span class="s1">&#39;limit&#39;</span><span class="p">:</span> <span class="n">limit</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="nb">filter</span><span class="p">:</span>
            <span class="n">query_variables</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">filter</span>

        <span class="n">graph_obj</span> <span class="o">=</span> <span class="n">GraphObject</span><span class="p">(</span>
            <span class="n">object_name</span><span class="o">=</span><span class="n">ASSETS_QUERY_OBJECT_NAME</span><span class="p">,</span>
            <span class="n">query</span><span class="o">=</span><span class="n">ASSETS_QUERY</span><span class="p">,</span>
            <span class="n">resp_schema</span><span class="o">=</span><span class="n">AssetsSchema</span><span class="p">,</span>
            <span class="n">query_variables</span><span class="o">=</span><span class="n">query_variables</span>
        <span class="p">)</span>

        <span class="k">return</span> <span class="n">OTGraphIterator</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="p">,</span> <span class="n">graph_obj</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.assets</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
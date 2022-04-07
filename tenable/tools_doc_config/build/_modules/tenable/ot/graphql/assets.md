
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ot.graphql.assets &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.assets</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ot.graphql.assets</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Assets GraphQL API.</span>
<span class="sd">For each class, please refer to the Tenable.ot documentation website for a</span>
<span class="sd">detailed explanation of the fields.</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">dataclasses</span> <span class="kn">import</span> <span class="n">dataclass</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span>
<span class="kn">from</span> <span class="nn">marshmallow.decorators</span> <span class="kn">import</span> <span class="n">post_load</span>
<span class="kn">from</span> <span class="nn">marshmallow.schema</span> <span class="kn">import</span> <span class="n">Schema</span>

<span class="n">ASSETS_QUERY_OBJECT_NAME</span> <span class="o">=</span> <span class="s1">&#39;assets&#39;</span>
<span class="n">ASSETS_QUERY</span> <span class="o">=</span> <span class="s1">&#39;&#39;&#39;</span>
<span class="s1">query assets($filter: AssetExpressionsParams, $search: String,</span>
<span class="s1">$sort: [AssetSortParams!]!, $limit: Int, $startAt: String) {</span>
<span class="s1">  assets(filter: $filter, search: $search, sort: $sort, first: $limit,</span>
<span class="s1">  after: $startAt){</span>
<span class="s1">    pageInfo{</span>
<span class="s1">      endCursor</span>
<span class="s1">    }</span>
<span class="s1">    nodes{</span>
<span class="s1">      id</span>
<span class="s1">      slot</span>
<span class="s1">      name</span>
<span class="s1">      type</span>
<span class="s1">      risk{</span>
<span class="s1">        unresolvedEvents</span>
<span class="s1">        totalRisk</span>
<span class="s1">      }</span>
<span class="s1">      criticality</span>
<span class="s1">      ips{</span>
<span class="s1">        nodes</span>
<span class="s1">      }</span>
<span class="s1">      macs{</span>
<span class="s1">        nodes</span>
<span class="s1">      }</span>
<span class="s1">      category</span>
<span class="s1">      vendor</span>
<span class="s1">      family</span>
<span class="s1">      model</span>
<span class="s1">      firmwareVersion</span>
<span class="s1">      os</span>
<span class="s1">      runStatus</span>
<span class="s1">      purdueLevel</span>
<span class="s1">      firstSeen</span>
<span class="s1">      lastSeen</span>
<span class="s1">      location</span>
<span class="s1">      backplane{</span>
<span class="s1">        id</span>
<span class="s1">        name</span>
<span class="s1">        size</span>
<span class="s1">      }</span>
<span class="s1">      description</span>
<span class="s1">      segments{</span>
<span class="s1">        nodes{</span>
<span class="s1">          id</span>
<span class="s1">          name</span>
<span class="s1">          type</span>
<span class="s1">          key</span>
<span class="s1">          systemName</span>
<span class="s1">          vlan</span>
<span class="s1">          description</span>
<span class="s1">          assetType</span>
<span class="s1">          subnet</span>
<span class="s1">        }</span>
<span class="s1">      }</span>
<span class="s1">    }</span>
<span class="s1">  }</span>
<span class="s1">}</span>
<span class="s1">&#39;&#39;&#39;</span>


<div class="viewcode-block" id="RiskSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.RiskSchema">[docs]</a><span class="k">class</span> <span class="nc">RiskSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving asset&#39;s risk information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">unresolved_events</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;unresolvedEvents&quot;</span><span class="p">)</span>
    <span class="n">total_risk</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Float</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;totalRisk&quot;</span><span class="p">)</span>

<div class="viewcode-block" id="RiskSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.RiskSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Risk</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>


<div class="viewcode-block" id="IpsSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.IpsSchema">[docs]</a><span class="k">class</span> <span class="nc">IpsSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving a list of IP addresses.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">nodes</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">())</span>

<div class="viewcode-block" id="IpsSchema.get_nodes"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.IpsSchema.get_nodes">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">get_nodes</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method returns the list inside &#39;nodes&#39; instead of an</span>
<span class="sd">        element.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">data</span><span class="p">[</span><span class="s1">&#39;nodes&#39;</span><span class="p">]</span></div></div>


<div class="viewcode-block" id="MacsSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.MacsSchema">[docs]</a><span class="k">class</span> <span class="nc">MacsSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving a list of MAC addresses.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">nodes</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">())</span>

<div class="viewcode-block" id="MacsSchema.get_nodes"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.MacsSchema.get_nodes">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">get_nodes</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method returns the list inside &#39;nodes&#39; instead of an</span>
<span class="sd">        element.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">data</span><span class="p">[</span><span class="s1">&#39;nodes&#39;</span><span class="p">]</span></div></div>


<div class="viewcode-block" id="BackplaneSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.BackplaneSchema">[docs]</a><span class="k">class</span> <span class="nc">BackplaneSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving backplane information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">size</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<div class="viewcode-block" id="BackplaneSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.BackplaneSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Backplane</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>


<div class="viewcode-block" id="SegmentSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.SegmentSchema">[docs]</a><span class="k">class</span> <span class="nc">SegmentSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving segment information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">key</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">system_name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;systemName&quot;</span><span class="p">)</span>
    <span class="n">vlan</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">description</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">asset_type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;assetType&quot;</span><span class="p">)</span>
    <span class="n">subnet</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<div class="viewcode-block" id="SegmentSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.SegmentSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Segment</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>


<div class="viewcode-block" id="SegmentsSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.SegmentsSchema">[docs]</a><span class="k">class</span> <span class="nc">SegmentsSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving a list of segments.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">nodes</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">SegmentSchema</span><span class="p">))</span>

<div class="viewcode-block" id="SegmentsSchema.get_nodes"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.SegmentsSchema.get_nodes">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">get_nodes</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method returns the list inside &#39;nodes&#39; instead of an</span>
<span class="sd">        element.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">data</span><span class="p">[</span><span class="s1">&#39;nodes&#39;</span><span class="p">]</span></div></div>


<div class="viewcode-block" id="AssetSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.AssetSchema">[docs]</a><span class="k">class</span> <span class="nc">AssetSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving asset information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">slot</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">risk</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">RiskSchema</span><span class="p">,</span> <span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">criticality</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">ips</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">IpsSchema</span><span class="p">,</span> <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">macs</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">MacsSchema</span><span class="p">,</span> <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">category</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">vendor</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">family</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">model</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">firmware_version</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;firmwareVersion&quot;</span><span class="p">)</span>
    <span class="n">os</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">run_status</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;runStatus&quot;</span><span class="p">)</span>
    <span class="n">purdue_level</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;purdueLevel&quot;</span><span class="p">)</span>
    <span class="n">first_seen</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;firstSeen&quot;</span><span class="p">)</span>
    <span class="n">last_seen</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">data_key</span><span class="o">=</span><span class="s2">&quot;lastSeen&quot;</span><span class="p">)</span>
    <span class="n">location</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">backplane</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">BackplaneSchema</span><span class="p">,</span> <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">description</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">segments</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">SegmentsSchema</span><span class="p">,</span> <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<div class="viewcode-block" id="AssetSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.AssetSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Asset</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>


<div class="viewcode-block" id="AssetsSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.AssetsSchema">[docs]</a><span class="k">class</span> <span class="nc">AssetsSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for retrieving a list of assets.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">nodes</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">AssetSchema</span><span class="p">))</span>

<div class="viewcode-block" id="AssetsSchema.get_nodes"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.AssetsSchema.get_nodes">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">get_nodes</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method returns the list inside &#39;nodes&#39; instead of an</span>
<span class="sd">        element.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">data</span><span class="p">[</span><span class="s1">&#39;nodes&#39;</span><span class="p">]</span></div></div>


<div class="viewcode-block" id="Risk"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Risk">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Risk</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds the risk information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">unresolved_events</span><span class="p">:</span> <span class="nb">int</span>
    <span class="n">total_risk</span><span class="p">:</span> <span class="nb">float</span></div>


<div class="viewcode-block" id="Ips"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Ips">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Ips</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds a list of IP addresses.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">ips</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span></div>


<div class="viewcode-block" id="Macs"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Macs">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Macs</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds a list of MAC addresses.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">macs</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span></div>


<div class="viewcode-block" id="Backplane"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Backplane">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Backplane</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds a backplane&#39;s information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">name</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">size</span><span class="p">:</span> <span class="nb">str</span></div>


<div class="viewcode-block" id="Segment"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Segment">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Segment</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds a segment&#39;s information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">name</span><span class="p">:</span> <span class="nb">str</span>
    <span class="nb">type</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">key</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">system_name</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">vlan</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">description</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">asset_type</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">subnet</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span></div>


<div class="viewcode-block" id="Asset"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.assets.Asset">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Asset</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds Tenable.ot asset information.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="nb">id</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">name</span><span class="p">:</span> <span class="nb">str</span>
    <span class="nb">type</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">risk</span><span class="p">:</span> <span class="n">Risk</span>
    <span class="n">criticality</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">category</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">purdue_level</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">slot</span><span class="p">:</span> <span class="nb">int</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">ips</span><span class="p">:</span> <span class="n">Ips</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">macs</span><span class="p">:</span> <span class="n">Macs</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">vendor</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">family</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">model</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">firmware_version</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">os</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">run_status</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">first_seen</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">last_seen</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">location</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">backplane</span><span class="p">:</span> <span class="n">Backplane</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">description</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">segments</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">Segment</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.assets</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
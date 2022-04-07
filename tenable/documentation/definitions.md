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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.definitions</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ot.graphql.definitions</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">GraphQL definitions file.</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">dataclasses</span> <span class="kn">import</span> <span class="n">dataclass</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span>
<span class="kn">from</span> <span class="nn">marshmallow.decorators</span> <span class="kn">import</span> <span class="n">post_load</span>
<span class="kn">from</span> <span class="nn">marshmallow.schema</span> <span class="kn">import</span> <span class="n">Schema</span>
<div class="viewcode-block" id="GraphObject"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.GraphObject">[docs]</a><span class="k">class</span> <span class="nc">GraphObject</span><span class="p">():</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    A class wrapper for the GraphQL query.</span>
<span class="sd">    This class can be further wrapped with other GraphObject classes that</span>
<span class="sd">    add more functionality to the original query.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">object_name</span><span class="p">,</span> <span class="n">query</span><span class="p">,</span> <span class="n">resp_schema</span><span class="p">,</span> <span class="n">query_variables</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_object_name</span> <span class="o">=</span> <span class="n">object_name</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_query</span> <span class="o">=</span> <span class="n">query</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_resp_schema</span> <span class="o">=</span> <span class="n">resp_schema</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_query_variables</span> <span class="o">=</span> <span class="n">query_variables</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">object_name</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The name of the GraphQL object that appears in the query.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_object_name</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">query</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The GraphQL query.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">resp_schema</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The expected response schema from the query.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_resp_schema</span>
    <span class="nd">@property</span>
    <span class="k">def</span> <span class="nf">query_variables</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The variables to pass to the query on call.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query_variables</span></div>
<div class="viewcode-block" id="GraphqlParsingError"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.GraphqlParsingError">[docs]</a><span class="k">class</span> <span class="nc">GraphqlParsingError</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    An error that&#39;s returned when a problem occurs parsing the Graphql response</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">message</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">message</span> <span class="o">=</span> <span class="n">message</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">()</span>
    <span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">message</span></div>
<div class="viewcode-block" id="LocationSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.LocationSchema">[docs]</a><span class="k">class</span> <span class="nc">LocationSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for GraphQL location part of the error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">line</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">column</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
<div class="viewcode-block" id="LocationSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.LocationSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Location</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>
<div class="viewcode-block" id="ExtensionsSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.ExtensionsSchema">[docs]</a><span class="k">class</span> <span class="nc">ExtensionsSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for GraphQL extensions part of the error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">code</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
<div class="viewcode-block" id="ExtensionsSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.ExtensionsSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">Extensions</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>
<div class="viewcode-block" id="GraphqlErrorSchema"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.GraphqlErrorSchema">[docs]</a><span class="k">class</span> <span class="nc">GraphqlErrorSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Schema for GraphQL error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">message</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">required</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">locations</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">LocationSchema</span><span class="p">))</span>
    <span class="n">path</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">())</span>
    <span class="n">extensions</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">ExtensionsSchema</span><span class="p">)</span>
<div class="viewcode-block" id="GraphqlErrorSchema.to_object"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.GraphqlErrorSchema.to_object">[docs]</a>    <span class="nd">@post_load</span>
    <span class="k">def</span> <span class="nf">to_object</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">data</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;This method turns the schema into its corresponding object.&#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="n">GraphqlError</span><span class="p">(</span><span class="o">**</span><span class="n">data</span><span class="p">)</span></div></div>
<div class="viewcode-block" id="Location"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.Location">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Location</span><span class="p">():</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds the location part of the error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">line</span><span class="p">:</span> <span class="nb">int</span>
    <span class="n">column</span><span class="p">:</span> <span class="nb">int</span></div>
<div class="viewcode-block" id="Extensions"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.Extensions">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">Extensions</span><span class="p">():</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds the extensions part of the error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">code</span><span class="p">:</span> <span class="nb">str</span> <span class="o">=</span> <span class="kc">None</span></div>
<div class="viewcode-block" id="GraphqlError"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.definitions.GraphqlError">[docs]</a><span class="nd">@dataclass</span>
<span class="k">class</span> <span class="nc">GraphqlError</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class holds a GraphQL error.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">message</span><span class="p">:</span> <span class="nb">str</span>
    <span class="n">locations</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">Location</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">path</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="n">extensions</span><span class="p">:</span> <span class="n">Extensions</span> <span class="o">=</span> <span class="kc">None</span>
    <span class="k">def</span> <span class="fm">__str__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="s1">&#39;</span><span class="si">{ret_code}</span><span class="s1">: </span><span class="si">{message}</span><span class="s1"> (</span><span class="si">{location}</span><span class="s1">), path </span><span class="si">{path}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="n">ret_code</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">extensions</span><span class="o">.</span><span class="n">code</span><span class="p">,</span>
            <span class="n">message</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">message</span><span class="p">,</span>
            <span class="n">location</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">locations</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
            <span class="n">path</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">path</span>
        <span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.definitions</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
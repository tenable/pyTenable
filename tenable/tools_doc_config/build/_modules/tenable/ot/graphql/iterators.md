
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ot.graphql.iterators &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.iterators</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ot.graphql.iterators</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">GraphQL Tenable.ot API iterator.</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">marshmallow.utils</span> <span class="kn">import</span> <span class="n">EXCLUDE</span>
<span class="kn">from</span> <span class="nn">restfly.iterator</span> <span class="kn">import</span> <span class="n">APIIterator</span>
<span class="kn">from</span> <span class="nn">tenable.ot.graphql.definitions</span> <span class="kn">import</span> <span class="p">(</span>
    <span class="n">GraphqlErrorSchema</span><span class="p">,</span>
    <span class="n">GraphqlParsingError</span>
<span class="p">)</span>


<div class="viewcode-block" id="OTGraphIterator"><a class="viewcode-back" href="../../../../tenable.ot.graphql.md#tenable.ot.graphql.iterators.OTGraphIterator">[docs]</a><span class="k">class</span> <span class="nc">OTGraphIterator</span><span class="p">(</span><span class="n">APIIterator</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Iterator class over Tenable.ot GraphQL connetions.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">api</span><span class="p">,</span> <span class="n">graph_object</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span> <span class="o">=</span> <span class="n">graph_object</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">api</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">_get_page</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the next page of data.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">graph_full_object</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;query&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">query</span><span class="p">,</span>
            <span class="s1">&#39;variables&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">query_variables</span>
        <span class="p">}</span>

        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">graphql</span><span class="p">(</span><span class="o">**</span><span class="n">graph_full_object</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;error&#39;</span> <span class="ow">in</span> <span class="n">resp</span><span class="p">:</span>
            <span class="n">errors</span> <span class="o">=</span> <span class="n">GraphqlErrorSchema</span><span class="p">(</span><span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
                <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;error&#39;</span><span class="p">][</span><span class="s1">&#39;errors&#39;</span><span class="p">],</span> <span class="n">unknown</span><span class="o">=</span><span class="n">EXCLUDE</span><span class="p">)</span>
            <span class="k">raise</span> <span class="n">errors</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;data&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">resp</span><span class="p">:</span>
            <span class="k">raise</span> <span class="n">GraphqlParsingError</span><span class="p">(</span>
                <span class="s1">&#39;graphql data field was not returned but no error occurred&#39;</span><span class="p">)</span>

        <span class="n">connection_object</span> <span class="o">=</span> <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;data&#39;</span><span class="p">][</span><span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">object_name</span><span class="p">]</span>
        <span class="k">if</span> <span class="n">connection_object</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
            <span class="k">raise</span> <span class="n">GraphqlParsingError</span><span class="p">(</span>
                <span class="sa">f</span><span class="s1">&#39;user requested object </span><span class="si">{</span><span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">object_name</span><span class="si">}</span><span class="s1">&#39;</span> <span class="o">+</span>
                <span class="s1">&#39; was not returned&#39;</span><span class="p">)</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">page</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">resp_schema</span><span class="p">()</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="n">connection_object</span><span class="p">,</span> <span class="n">unknown</span><span class="o">=</span><span class="n">EXCLUDE</span><span class="p">)</span>

        <span class="bp">self</span><span class="o">.</span><span class="n">_graph_object</span><span class="o">.</span><span class="n">query_variables</span><span class="p">[</span><span class="s1">&#39;startAt&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">connection_object</span><span class="p">[</span>
            <span class="s1">&#39;pageInfo&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;endCursor&#39;</span><span class="p">,</span> <span class="kc">None</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">page</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ot.graphql.iterators</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>

<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.checker.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.checker.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Checker</span>
<span class="sd">=======</span>

<span class="sd">Methods described in this section relate to the the checker API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.checker``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: CheckerAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.checker.schema</span> <span class="kn">import</span> <span class="n">CheckerSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>


<div class="viewcode-block" id="CheckerAPI"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.api.CheckerAPI">[docs]</a><span class="k">class</span> <span class="nc">CheckerAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;checkers&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">CheckerSchema</span><span class="p">()</span>

<div class="viewcode-block" id="CheckerAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.api.CheckerAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of checkers.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                A list of checkers.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.checker.list()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="CheckerAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.api.CheckerAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">checker_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Gets the details of the particular checker based on checker</span>
<span class="sd">        identifier.</span>

<span class="sd">        Args:</span>
<span class="sd">            checker_id (str): The checker instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                Details of the given ``checker_id``.</span>

<span class="sd">        Examples:</span>

<span class="sd">            &gt;&gt;&gt; tad.checker.details(checker_id=&#39;1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">checker_id</span><span class="si">}</span><span class="s1">&#39;</span><span class="p">))</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
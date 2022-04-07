
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.checker.schema &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker.schema</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.checker.schema</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span>
<span class="kn">from</span> <span class="nn">tenable.ad.base.schema</span> <span class="kn">import</span> <span class="n">CamelCaseSchema</span>


<div class="viewcode-block" id="AttackerKnownToolSchema"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.schema.AttackerKnownToolSchema">[docs]</a><span class="k">class</span> <span class="nc">AttackerKnownToolSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">url</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">author</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">link</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span></div>


<div class="viewcode-block" id="ResourcesSchema"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.schema.ResourcesSchema">[docs]</a><span class="k">class</span> <span class="nc">ResourcesSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">url</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span></div>


<div class="viewcode-block" id="VulnerabilityDetailSchema"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.schema.VulnerabilityDetailSchema">[docs]</a><span class="k">class</span> <span class="nc">VulnerabilityDetailSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">detail</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>


<div class="viewcode-block" id="RecommendationSchema"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.schema.RecommendationSchema">[docs]</a><span class="k">class</span> <span class="nc">RecommendationSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">description</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">exec_summary</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">detail</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">resources</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">ResourcesSchema</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">attacker_known_tools</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">AttackerKnownToolSchema</span><span class="p">,</span>
                                         <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>


<div class="viewcode-block" id="CheckerSchema"><a class="viewcode-back" href="../../../../tenable.ad.checker.md#tenable.ad.checker.schema.CheckerSchema">[docs]</a><span class="k">class</span> <span class="nc">CheckerSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">codename</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">remediation_cost</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">category_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">name</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">description</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">exec_summary</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">vulnerability_detail</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">VulnerabilityDetailSchema</span><span class="p">)</span>
    <span class="n">attacker_known_tools</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">AttackerKnownToolSchema</span><span class="p">,</span>
                                         <span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">resources</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">ResourcesSchema</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">recommendation</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">RecommendationSchema</span><span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker.schema</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>

<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.score.schema &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score.schema</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.score.schema</h1><div class="highlight"><pre>
<span></span><span class="kn">import</span> <span class="nn">typing</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span><span class="p">,</span> <span class="n">ValidationError</span>
<span class="kn">from</span> <span class="nn">tenable.ad.base.schema</span> <span class="kn">import</span> <span class="n">CamelCaseSchema</span>


<div class="viewcode-block" id="ScoreRules"><a class="viewcode-back" href="../../../../tenable.ad.score.md#tenable.ad.score.schema.ScoreRules">[docs]</a><span class="k">class</span> <span class="nc">ScoreRules</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Field</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_deserialize</span><span class="p">(</span>
            <span class="bp">self</span><span class="p">,</span>
            <span class="n">value</span><span class="p">:</span> <span class="n">typing</span><span class="o">.</span><span class="n">Any</span><span class="p">,</span>
            <span class="n">attr</span><span class="p">:</span> <span class="n">typing</span><span class="o">.</span><span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">],</span>
            <span class="n">data</span><span class="p">:</span> <span class="n">typing</span><span class="o">.</span><span class="n">Optional</span><span class="p">[</span><span class="n">typing</span><span class="o">.</span><span class="n">Mapping</span><span class="p">[</span><span class="nb">str</span><span class="p">,</span> <span class="n">typing</span><span class="o">.</span><span class="n">Any</span><span class="p">]],</span>
            <span class="o">**</span><span class="n">kwargs</span>
    <span class="p">):</span>
        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="nb">list</span><span class="p">)</span> <span class="ow">or</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="nb">str</span><span class="p">):</span>
            <span class="k">return</span> <span class="n">value</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="k">raise</span> <span class="n">ValidationError</span><span class="p">(</span><span class="s1">&#39;Field should be string or list&#39;</span><span class="p">)</span></div>


<div class="viewcode-block" id="ScoreSchema"><a class="viewcode-back" href="../../../../tenable.ad.score.md#tenable.ad.score.schema.ScoreSchema">[docs]</a><span class="k">class</span> <span class="nc">ScoreSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">profile_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">directory_ids</span> <span class="o">=</span> <span class="n">ScoreRules</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">checker_ids</span> <span class="o">=</span> <span class="n">ScoreRules</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">reason_ids</span> <span class="o">=</span> <span class="n">ScoreRules</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
    <span class="n">directory_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">score</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">(</span><span class="n">allow_none</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score.schema</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
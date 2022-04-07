
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.widget.schema &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.widget.schema</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.widget.schema</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span><span class="p">,</span> <span class="n">validate</span> <span class="k">as</span> <span class="n">v</span>
<span class="kn">from</span> <span class="nn">tenable.ad.base.schema</span> <span class="kn">import</span> <span class="n">CamelCaseSchema</span>


<div class="viewcode-block" id="WidgetDataOptionsSchema"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.schema.WidgetDataOptionsSchema">[docs]</a><span class="k">class</span> <span class="nc">WidgetDataOptionsSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">duration</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">interval</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">active</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Bool</span><span class="p">()</span>
    <span class="n">directory_ids</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">())</span>
    <span class="n">profile_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">checker_ids</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">())</span>
    <span class="n">reason_ids</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">List</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">())</span></div>


<div class="viewcode-block" id="WidgetDisplayOptionsSchema"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.schema.WidgetDisplayOptionsSchema">[docs]</a><span class="k">class</span> <span class="nc">WidgetDisplayOptionsSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">label</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">category_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span></div>


<div class="viewcode-block" id="WidgetSeriesSchema"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.schema.WidgetSeriesSchema">[docs]</a><span class="k">class</span> <span class="nc">WidgetSeriesSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="n">data_options</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">WidgetDataOptionsSchema</span><span class="p">)</span>
    <span class="n">display_options</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">WidgetDisplayOptionsSchema</span><span class="p">)</span></div>


<div class="viewcode-block" id="WidgetOptionSchema"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.schema.WidgetOptionSchema">[docs]</a><span class="k">class</span> <span class="nc">WidgetOptionSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="nb">type</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">(</span>
        <span class="n">validate</span><span class="o">=</span><span class="n">v</span><span class="o">.</span><span class="n">OneOf</span><span class="p">([</span><span class="s1">&#39;BigNumber&#39;</span><span class="p">,</span> <span class="s1">&#39;LineChart&#39;</span><span class="p">,</span> <span class="s1">&#39;BarChart&#39;</span><span class="p">,</span>
                          <span class="s1">&#39;SecurityCompliance&#39;</span><span class="p">,</span> <span class="s1">&#39;StepChart&#39;</span><span class="p">]))</span>
    <span class="n">series</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Nested</span><span class="p">(</span><span class="n">WidgetSeriesSchema</span><span class="p">,</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>


<div class="viewcode-block" id="WidgetSchema"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.schema.WidgetSchema">[docs]</a><span class="k">class</span> <span class="nc">WidgetSchema</span><span class="p">(</span><span class="n">CamelCaseSchema</span><span class="p">):</span>
    <span class="nb">id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">widget_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">dashboard_id</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">title</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Str</span><span class="p">()</span>
    <span class="n">pos_x</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">pos_y</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">width</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span>
    <span class="n">height</span> <span class="o">=</span> <span class="n">fields</span><span class="o">.</span><span class="n">Int</span><span class="p">()</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.widget.schema</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
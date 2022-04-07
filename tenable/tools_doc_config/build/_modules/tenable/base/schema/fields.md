
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.base.schema.fields &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.schema.fields</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.base.schema.fields</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Extended field definitions</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">fields</span>


<div class="viewcode-block" id="BaseField"><a class="viewcode-back" href="../../../../tenable.base.schema.md#tenable.base.schema.fields.BaseField">[docs]</a><span class="k">class</span> <span class="nc">BaseField</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Field</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    BaseField Field</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">inner</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">inner</span> <span class="o">=</span> <span class="n">inner</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

    <span class="k">def</span> <span class="nf">_bind_to_schema</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">field_name</span><span class="p">,</span> <span class="n">parent</span><span class="p">):</span>  <span class="c1"># noqa PLW0221</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_bind_to_schema</span><span class="p">(</span><span class="n">field_name</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">inner</span><span class="o">.</span><span class="n">_bind_to_schema</span><span class="p">(</span><span class="n">field_name</span><span class="p">,</span> <span class="n">parent</span><span class="p">)</span>  <span class="c1"># noqa PLW0212</span>

    <span class="k">def</span> <span class="nf">_deserialize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">inner</span><span class="o">.</span><span class="n">_deserialize</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>  <span class="c1"># noqa PLW0212</span>

    <span class="k">def</span> <span class="nf">_serialize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">inner</span><span class="o">.</span><span class="n">_serialize</span><span class="p">(</span><span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>  <span class="c1"># noqa PLW0212</span></div>


<div class="viewcode-block" id="LowerCase"><a class="viewcode-back" href="../../../../tenable.base.schema.md#tenable.base.schema.fields.LowerCase">[docs]</a><span class="k">class</span> <span class="nc">LowerCase</span><span class="p">(</span><span class="n">BaseField</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The field value will be lower-cased with this field.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="nf">_deserialize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="s1">&#39;lower&#39;</span><span class="p">):</span>
            <span class="n">value</span> <span class="o">=</span> <span class="n">value</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">return</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_deserialize</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span></div>


<div class="viewcode-block" id="UpperCase"><a class="viewcode-back" href="../../../../tenable.base.schema.md#tenable.base.schema.fields.UpperCase">[docs]</a><span class="k">class</span> <span class="nc">UpperCase</span><span class="p">(</span><span class="n">BaseField</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The field value will be upper-cased with this field.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="nf">_deserialize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="s1">&#39;upper&#39;</span><span class="p">):</span>
            <span class="n">value</span> <span class="o">=</span> <span class="n">value</span><span class="o">.</span><span class="n">upper</span><span class="p">()</span>
        <span class="k">return</span> <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="n">_deserialize</span><span class="p">(</span><span class="n">value</span><span class="p">,</span> <span class="o">*</span><span class="n">args</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.schema.fields</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>

<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.base.utils.envelope &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.utils.envelope</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.base.utils.envelope</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Dictionary enveloping utility.</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Optional</span><span class="p">,</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>


<div class="viewcode-block" id="envelope"><a class="viewcode-back" href="../../../../tenable.base.utils.md#tenable.base.utils.envelope.envelope">[docs]</a><span class="k">def</span> <span class="nf">envelope</span><span class="p">(</span><span class="n">data</span><span class="p">:</span> <span class="n">Dict</span><span class="p">,</span>
             <span class="n">key</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
             <span class="n">excludes</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]]</span> <span class="o">=</span> <span class="kc">None</span>
             <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Reformats the data dictionary to push any keys that aren&#39;t described in the</span>
<span class="sd">    excludes list into the filters sub-object.</span>

<span class="sd">    Args:</span>
<span class="sd">        data (dict):</span>
<span class="sd">            The data dictionary to modify</span>
<span class="sd">        key (str):</span>
<span class="sd">            The dictionary key to wrap the data within.</span>
<span class="sd">        excludes (list[str], optional):</span>
<span class="sd">            A list of keys to exclude from the enveloping process.</span>

<span class="sd">    Returns:</span>
<span class="sd">        dict:</span>
<span class="sd">            The modified data dictionary.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">resp</span> <span class="o">=</span> <span class="p">{}</span>

    <span class="c1"># for each excluded item, we will move it into the response dictionary</span>
    <span class="c1"># using the same key.</span>
    <span class="k">if</span> <span class="n">excludes</span><span class="p">:</span>
        <span class="k">for</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">excludes</span><span class="p">:</span>
            <span class="k">if</span> <span class="n">item</span> <span class="ow">in</span> <span class="n">data</span><span class="p">:</span>
                <span class="n">resp</span><span class="p">[</span><span class="n">item</span><span class="p">]</span> <span class="o">=</span> <span class="n">data</span><span class="o">.</span><span class="n">pop</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>

    <span class="c1"># add the remaining attributes in the data dictionary to the response</span>
    <span class="c1"># object within the envelope key.</span>
    <span class="n">resp</span><span class="p">[</span><span class="n">key</span><span class="p">]</span> <span class="o">=</span> <span class="n">data</span>

    <span class="c1"># Return the response object to the caller.</span>
    <span class="k">return</span> <span class="n">resp</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.utils.envelope</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
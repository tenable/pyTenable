<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../genindex.md" />
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.utils</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.utils</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">restfly.utils</span> <span class="kn">import</span> <span class="n">dict_clean</span><span class="p">,</span> <span class="n">dict_merge</span><span class="p">,</span> <span class="n">url_validator</span>  <span class="c1"># noqa: F401</span>
<div class="viewcode-block" id="policy_settings"><a class="viewcode-back" href="../../README.md#tenable.utils.policy_settings">[docs]</a><span class="k">def</span> <span class="nf">policy_settings</span><span class="p">(</span><span class="n">item</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Recursive function to attempt to pull out the various settings from scan</span>
<span class="sd">    policy settings in the editor format.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">resp</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
    <span class="k">if</span> <span class="s1">&#39;id&#39;</span> <span class="ow">in</span> <span class="n">item</span> <span class="ow">and</span> <span class="p">(</span>
        <span class="s1">&#39;default&#39;</span> <span class="ow">in</span> <span class="n">item</span>
        <span class="ow">or</span> <span class="p">(</span>
            <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">item</span>
            <span class="ow">and</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span>
            <span class="ow">in</span> <span class="p">[</span>
                <span class="s1">&#39;file&#39;</span><span class="p">,</span>
                <span class="s1">&#39;checkbox&#39;</span><span class="p">,</span>
                <span class="s1">&#39;entry&#39;</span><span class="p">,</span>
                <span class="s1">&#39;textarea&#39;</span><span class="p">,</span>
                <span class="s1">&#39;medium-fixed-entry&#39;</span><span class="p">,</span>
                <span class="s1">&#39;password&#39;</span><span class="p">,</span>
            <span class="p">]</span>
        <span class="p">)</span>
    <span class="p">):</span>
        <span class="c1"># if we find both an &#39;id&#39; and a &#39;default&#39; attribute, or if we find</span>
        <span class="c1"># a &#39;type&#39; attribute matching one of the known attribute types, then</span>
        <span class="c1"># we will parse out the data and append it to the response dictionary</span>
        <span class="k">if</span> <span class="s1">&#39;default&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">item</span><span class="p">:</span>
            <span class="n">item</span><span class="p">[</span><span class="s1">&#39;default&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span>
        <span class="n">resp</span><span class="p">[</span><span class="n">item</span><span class="p">[</span><span class="s1">&#39;id&#39;</span><span class="p">]]</span> <span class="o">=</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;default&#39;</span><span class="p">]</span>
    <span class="k">for</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">item</span><span class="o">.</span><span class="n">keys</span><span class="p">():</span>
        <span class="c1"># here we will attempt to recurse down both a list of sub-</span>
        <span class="c1"># documents and an explicitly defined sub-document within the</span>
        <span class="c1"># editor data-structure.</span>
        <span class="k">if</span> <span class="n">key</span> <span class="o">==</span> <span class="s1">&#39;modes&#39;</span><span class="p">:</span>
            <span class="k">continue</span>
        <span class="k">if</span> <span class="p">(</span>
            <span class="nb">isinstance</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">],</span> <span class="nb">list</span><span class="p">)</span>
            <span class="ow">and</span> <span class="nb">len</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span>
            <span class="ow">and</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">][</span><span class="mi">0</span><span class="p">],</span> <span class="nb">dict</span><span class="p">)</span>
        <span class="p">):</span>
            <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">]:</span>
                <span class="n">resp</span> <span class="o">=</span> <span class="n">dict_merge</span><span class="p">(</span><span class="n">resp</span><span class="p">,</span> <span class="n">policy_settings</span><span class="p">(</span><span class="n">i</span><span class="p">))</span>
        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">],</span> <span class="nb">dict</span><span class="p">):</span>
            <span class="n">resp</span> <span class="o">=</span> <span class="n">dict_merge</span><span class="p">(</span><span class="n">resp</span><span class="p">,</span> <span class="n">policy_settings</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="n">key</span><span class="p">]))</span>
    <span class="c1"># Return the key-value pair.</span>
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
          <a href="../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.utils</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
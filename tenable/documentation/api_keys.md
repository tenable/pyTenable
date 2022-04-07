<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../genindex.md" />
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.api_keys</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.api_keys</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">APIKeys</span>
<span class="sd">=======</span>
<span class="sd">Methods described in this section relate to the the APIKeys API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.api_keys``.</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: APIKeyAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<div class="viewcode-block" id="APIKeyAPI"><a class="viewcode-back" href="../../../tenable.ad.md#tenable.ad.api_keys.APIKeyAPI">[docs]</a><span class="k">class</span> <span class="nc">APIKeyAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;api-key&#39;</span>
<div class="viewcode-block" id="APIKeyAPI.get"><a class="viewcode-back" href="../../../tenable.ad.md#tenable.ad.api_keys.APIKeyAPI.get">[docs]</a>    <span class="k">def</span> <span class="nf">get</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Gets the API Key of the current user.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.api_keys.get()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="n">box</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span><span class="o">.</span><span class="n">key</span></div>
<div class="viewcode-block" id="APIKeyAPI.refresh"><a class="viewcode-back" href="../../../tenable.ad.md#tenable.ad.api_keys.APIKeyAPI.refresh">[docs]</a>    <span class="k">def</span> <span class="nf">refresh</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">str</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates or renews an API for the current user.  Will also refresh the</span>
<span class="sd">        API Key used in the current TenableAD session.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.api_keys.refresh()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">key</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="p">{},</span> <span class="n">box</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span><span class="o">.</span><span class="n">key</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">_key_auth</span><span class="p">(</span><span class="n">key</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">key</span></div></div>
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
          <a href="../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.api_keys</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
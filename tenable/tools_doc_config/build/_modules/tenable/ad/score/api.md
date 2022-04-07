
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.score.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.score.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Score</span>
<span class="sd">=====</span>

<span class="sd">Methods described in this section relate to the the score API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.score``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScoreAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.score.schema</span> <span class="kn">import</span> <span class="n">ScoreSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>


<div class="viewcode-block" id="ScoreAPI"><a class="viewcode-back" href="../../../../tenable.ad.score.md#tenable.ad.score.api.ScoreAPI">[docs]</a><span class="k">class</span> <span class="nc">ScoreAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">ScoreSchema</span><span class="p">()</span>

<div class="viewcode-block" id="ScoreAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.score.md#tenable.ad.score.api.ScoreAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
             <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
             <span class="o">**</span><span class="n">kwargs</span>
             <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Get the list of directories score by profile.</span>

<span class="sd">        Args:</span>
<span class="sd">            Option-1:</span>
<span class="sd">                profile_id (str):</span>
<span class="sd">                    The profile instance identifier.</span>
<span class="sd">                directory_ids (optional, List(int)):</span>
<span class="sd">                    The list of directory_ids.</span>
<span class="sd">                checker_ids (optional, List(int)):</span>
<span class="sd">                    The list of checker_ids.</span>
<span class="sd">                reason_ids (optional, List(int)):</span>
<span class="sd">                    The list of reason_ids.</span>

<span class="sd">            Option-2:</span>
<span class="sd">                profile_id (str):</span>
<span class="sd">                    The profile instance identifier.</span>
<span class="sd">                directory_ids (optional, str):</span>
<span class="sd">                    The directory_id instance identifier.</span>
<span class="sd">                checker_ids (optional, str):</span>
<span class="sd">                    The checker_id instance identifier.</span>
<span class="sd">                reason_ids (optional, str):</span>
<span class="sd">                    The reason_id instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                List of scores of different directories in the instance.</span>

<span class="sd">        Examples:</span>

<span class="sd">            With single directory_ids, checker_ids, reason_ids</span>

<span class="sd">            &gt;&gt;&gt; tad.score.list(profile_id=&#39;1&#39;,</span>
<span class="sd">            ...     directory_ids=&#39;3&#39;,</span>
<span class="sd">            ...     checker_ids=&#39;1&#39;,</span>
<span class="sd">            ...     reason_ids=&#39;1&#39;)</span>

<span class="sd">            With multiple directory_ids, checker_ids, reason_ids</span>

<span class="sd">            &gt;&gt;&gt; tad.score.list(profile_id=&#39;1&#39;,</span>
<span class="sd">            ...     directory_ids=[1, 2, 3],</span>
<span class="sd">            ...     checker_ids=[1, 2, 3],</span>
<span class="sd">            ...     reason_ids=[1, 2, 3])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">param</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;directoryIds&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;directory_ids&#39;</span><span class="p">),</span>
            <span class="s1">&#39;checkerIds&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;checker_ids&#39;</span><span class="p">),</span>
            <span class="s1">&#39;reasonIds&#39;</span><span class="p">:</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;reason_ids&#39;</span><span class="p">)</span>
        <span class="p">}))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;profiles/</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">/scores&#39;</span><span class="p">,</span>
                                               <span class="n">params</span><span class="o">=</span><span class="n">param</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.score.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
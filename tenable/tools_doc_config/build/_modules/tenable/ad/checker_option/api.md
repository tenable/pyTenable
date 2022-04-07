
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.checker_option.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker_option.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.checker_option.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Checker Option</span>
<span class="sd">==============</span>

<span class="sd">Methods described in this section relate to the the checker option API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.checker_option``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: CheckerOptionAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.checker_option.schema</span> <span class="kn">import</span> <span class="n">CheckerOptionSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>


<div class="viewcode-block" id="CheckerOptionAPI"><a class="viewcode-back" href="../../../../tenable.ad.checker_option.md#tenable.ad.checker_option.api.CheckerOptionAPI">[docs]</a><span class="k">class</span> <span class="nc">CheckerOptionAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">CheckerOptionSchema</span><span class="p">()</span>

<div class="viewcode-block" id="CheckerOptionAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.checker_option.md#tenable.ad.checker_option.api.CheckerOptionAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
             <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
             <span class="n">checker_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
             <span class="o">**</span><span class="n">kwargs</span>
             <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of checker-options.</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>
<span class="sd">            checker_id (str):</span>
<span class="sd">                The checker instance identifier.</span>
<span class="sd">            staged (optional, bool):</span>
<span class="sd">                Get only the checker-options that are staged. Accepted</span>
<span class="sd">                values are ``True`` and ``False``. Added checker options</span>
<span class="sd">                are first staged until the profile is commited. The staged</span>
<span class="sd">                profile options are not activated and don&#39;t affect</span>
<span class="sd">                yet the IOE and the exposure detection.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                List of checker options.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.checker_option.list(</span>
<span class="sd">            ...     profile_id=&#39;9&#39;,</span>
<span class="sd">            ...     checker_id=&#39;1&#39;,</span>
<span class="sd">            ...     staged=True</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">,</span> <span class="n">partial</span><span class="o">=</span><span class="kc">True</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                <span class="sa">f</span><span class="s1">&#39;profiles/</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">/checkers/</span><span class="si">{</span><span class="n">checker_id</span><span class="si">}</span><span class="s1">/checker-options&#39;</span><span class="p">,</span>
                <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div>

<div class="viewcode-block" id="CheckerOptionAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.checker_option.md#tenable.ad.checker_option.api.CheckerOptionAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">profile_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">checker_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates the new checker-option.</span>

<span class="sd">        Args:</span>
<span class="sd">            profile_id (str):</span>
<span class="sd">                The profile instance identifier.</span>
<span class="sd">            checker_id (str):</span>
<span class="sd">                The checker instance identifier.</span>
<span class="sd">            codename (str):</span>
<span class="sd">                The codename of the checker option.</span>
<span class="sd">            value (str):</span>
<span class="sd">                The value of the checker option.</span>
<span class="sd">            value_type (str):</span>
<span class="sd">                The type of the checker option. Accepted values are:</span>
<span class="sd">                ``string``, ``regex``, ``float``, ``integer``, ``boolean``,</span>
<span class="sd">                ``date``, ``object``, ``array/string``, ``array/regex``,</span>
<span class="sd">                ``array/integer``, ``array/boolean``, ``array/select``,</span>
<span class="sd">                ``array/object``.</span>
<span class="sd">            directory_id (optional, int):</span>
<span class="sd">                The directory instance identifier.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                Created checker option instance.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.checker_option.create(</span>
<span class="sd">            ...     profile_id=&#39;9&#39;,</span>
<span class="sd">            ...     checker_id=&#39;2&#39;,</span>
<span class="sd">            ...     codename=&#39;codename&#39;,</span>
<span class="sd">            ...     value=&#39;false&#39;,</span>
<span class="sd">            ...     value_type=&#39;boolean&#39;</span>
<span class="sd">            ...     directory_id=3</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))]</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span>
                <span class="sa">f</span><span class="s1">&#39;profiles/</span><span class="si">{</span><span class="n">profile_id</span><span class="si">}</span><span class="s1">/checkers/</span><span class="si">{</span><span class="n">checker_id</span><span class="si">}</span><span class="s1">/checker-options&#39;</span><span class="p">,</span>
                <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">),</span> <span class="n">many</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.checker_option.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
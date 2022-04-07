
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.ad.preference.api &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.preference.api</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.ad.preference.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Preference</span>
<span class="sd">=============</span>

<span class="sd">Methods described in this section relate to the preferences API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.preference``.</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: PreferenceAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">PreferenceSchema</span>


<div class="viewcode-block" id="PreferenceAPI"><a class="viewcode-back" href="../../../../tenable.ad.preference.md#tenable.ad.preference.api.PreferenceAPI">[docs]</a><span class="k">class</span> <span class="nc">PreferenceAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;preferences&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">PreferenceSchema</span><span class="p">()</span>

<div class="viewcode-block" id="PreferenceAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.preference.md#tenable.ad.preference.api.PreferenceAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Get the user&#39;s preferences</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The user&#39;s preferences object</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.preference.details()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">())</span></div>

<div class="viewcode-block" id="PreferenceAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.preference.md#tenable.ad.preference.api.PreferenceAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update the user&#39;s preferences</span>

<span class="sd">        Args:</span>
<span class="sd">            language (optional, str):</span>
<span class="sd">                The language of product for the current user.</span>
<span class="sd">            preferred_profile_id (optional, int):</span>
<span class="sd">                The profile identifier to use after login for the current user.</span>

<span class="sd">        Return:</span>
<span class="sd">            The user&#39;s preferences object</span>

<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.preference.update(</span>
<span class="sd">            ...     language=&#39;en&#39;,</span>
<span class="sd">            ...     preferred_profile_id=1</span>
<span class="sd">            ... )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.preference.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
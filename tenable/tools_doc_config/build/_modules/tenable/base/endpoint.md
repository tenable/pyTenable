
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.base.endpoint &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../../_static/custom.css" />
    
    <script data-url_root="../../../" id="documentation_options" src="../../../_static/documentation_options.js"></script>
    <script src="../../../_static/jquery.js"></script>
    <script src="../../../_static/underscore.js"></script>
    <script src="../../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../../genindex.md" />
    <link rel="search" title="Search" href="../../../search.md" /> 
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.endpoint</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.base.endpoint</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Base Endpoint</span>
<span class="sd">=============</span>

<span class="sd">The APIEndpoint class is the base class that all endpoint modules will inherit</span>
<span class="sd">from.  Throughout pyTenable v1, packages will be transitioning to using this</span>
<span class="sd">base class over the original APISession class.</span>

<span class="sd">.. autoclass:: APIEndpoint</span>
<span class="sd">    :members:</span>
<span class="sd">    :inherited-members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Any</span><span class="p">,</span> <span class="n">List</span><span class="p">,</span> <span class="n">Optional</span>
<span class="kn">from</span> <span class="nn">restfly.utils</span> <span class="kn">import</span> <span class="n">check</span>
<span class="kn">from</span> <span class="nn">restfly</span> <span class="kn">import</span> <span class="n">APIEndpoint</span> <span class="k">as</span> <span class="n">Base</span>


<div class="viewcode-block" id="APIEndpoint"><a class="viewcode-back" href="../../../tenable.base.md#tenable.base.endpoint.APIEndpoint">[docs]</a><span class="k">class</span> <span class="nc">APIEndpoint</span><span class="p">(</span><span class="n">Base</span><span class="p">):</span>  <span class="c1"># noqa PLR0903</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Base API Endpoint class</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="nf">_check</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>  <span class="c1"># noqa PLR0913</span>
               <span class="n">name</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
               <span class="n">obj</span><span class="p">:</span> <span class="n">Any</span><span class="p">,</span>
               <span class="n">expected_type</span><span class="p">:</span> <span class="n">Any</span><span class="p">,</span>
               <span class="n">choices</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">List</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
               <span class="n">default</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">Any</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
               <span class="n">case</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">,</span>
               <span class="n">pattern</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Any</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Overload for RESTfly&#39;s check function to make it behave like the old</span>
<span class="sd">        _check method.</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The display name of the attribute to be checked</span>
<span class="sd">            obj (Any):</span>
<span class="sd">                The object to check.</span>
<span class="sd">            expected_type (Any):</span>
<span class="sd">                The object type to check against</span>
<span class="sd">            choices (optional, list[Any]):</span>
<span class="sd">                A list of valid values that `obj` must be.</span>
<span class="sd">            default (optional, Any):</span>
<span class="sd">                The default value to return if the `obj` is `None`.</span>
<span class="sd">            case (optional, str):</span>
<span class="sd">                If the expected_type is `str`, should the resp be uppercased</span>
<span class="sd">                or lowercased?  Valid values are `upper` and `lower`.</span>
<span class="sd">            pattern (optional, str):</span>
<span class="sd">                A regex pattern to match the `obj` against if it is of a `str`</span>
<span class="sd">                type.</span>

<span class="sd">        Raises:</span>
<span class="sd">            TypeError:</span>
<span class="sd">                If the `obj` is not the expected_type, then raise a `TypeError`</span>
<span class="sd">            UnexpectedValueError:</span>
<span class="sd">                If the `obj` fails either the regex pattern or choices checks,</span>
<span class="sd">                then an UnexpectedValueError is raises.</span>

<span class="sd">        Returns:</span>
<span class="sd">            Any:</span>
<span class="sd">                Will return the object passed if all the checks succeed.  If a</span>
<span class="sd">                default parameter was set and the object was a NoneType, then</span>
<span class="sd">                the default value will be returned instead.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">pattern_map</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;scanner-uuid&#39;</span><span class="p">:</span> <span class="p">(</span><span class="sa">r</span><span class="s1">&#39;^[a-fA-F0-9]</span><span class="si">{8}</span><span class="s1">-&#39;</span>
                             <span class="sa">r</span><span class="s1">&#39;[a-fA-F0-9]</span><span class="si">{4}</span><span class="s1">-&#39;</span>
                             <span class="sa">r</span><span class="s1">&#39;[a-fA-F0-9]</span><span class="si">{4}</span><span class="s1">-&#39;</span>
                             <span class="sa">r</span><span class="s1">&#39;[a-fA-F0-9]</span><span class="si">{4}</span><span class="s1">-&#39;</span>
                             <span class="sa">r</span><span class="s1">&#39;[a-fA-F0-9]{12,32}$&#39;</span>
                             <span class="p">)</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="n">expected_type</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;uuid&#39;</span><span class="p">,</span> <span class="s1">&#39;scanner-uuid&#39;</span><span class="p">]:</span>
            <span class="k">return</span> <span class="n">check</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">name</span><span class="p">,</span>
                         <span class="n">obj</span><span class="o">=</span><span class="n">obj</span><span class="p">,</span>
                         <span class="n">expected_type</span><span class="o">=</span><span class="nb">str</span><span class="p">,</span>
                         <span class="n">pattern</span><span class="o">=</span><span class="n">expected_type</span><span class="p">,</span>
                         <span class="n">case</span><span class="o">=</span><span class="n">case</span><span class="p">,</span>
                         <span class="n">choices</span><span class="o">=</span><span class="n">choices</span><span class="p">,</span>
                         <span class="n">default</span><span class="o">=</span><span class="n">default</span><span class="p">,</span>
                         <span class="n">pattern_map</span><span class="o">=</span><span class="n">pattern_map</span>
                         <span class="p">)</span>
        <span class="k">return</span> <span class="n">check</span><span class="p">(</span><span class="n">name</span><span class="o">=</span><span class="n">name</span><span class="p">,</span>
                     <span class="n">obj</span><span class="o">=</span><span class="n">obj</span><span class="p">,</span>
                     <span class="n">expected_type</span><span class="o">=</span><span class="n">expected_type</span><span class="p">,</span>
                     <span class="n">regex</span><span class="o">=</span><span class="n">pattern</span><span class="p">,</span>
                     <span class="n">case</span><span class="o">=</span><span class="n">case</span><span class="p">,</span>
                     <span class="n">choices</span><span class="o">=</span><span class="n">choices</span><span class="p">,</span>
                     <span class="n">default</span><span class="o">=</span><span class="n">default</span><span class="p">,</span>
                     <span class="n">pattern_map</span><span class="o">=</span><span class="n">pattern_map</span>
                     <span class="p">)</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.base.endpoint</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
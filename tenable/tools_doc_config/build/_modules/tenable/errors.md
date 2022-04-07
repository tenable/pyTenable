
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.errors &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/custom.css" />
    
    <script data-url_root="../../" id="documentation_options" src="../../_static/documentation_options.js"></script>
    <script src="../../_static/jquery.js"></script>
    <script src="../../_static/underscore.js"></script>
    <script src="../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../genindex.md" />
    <link rel="search" title="Search" href="../../search.md" /> 
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
        <li class="nav-item nav-item-this"><a href="">tenable.errors</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.errors</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">.. autoclass:: AuthenticationWarning</span>
<span class="sd">.. autoclass:: FileDownloadError</span>
<span class="sd">.. autoclass:: ImpersonationError</span>
<span class="sd">.. autoclass:: PasswordComplexityError</span>
<span class="sd">.. autoclass:: TioExportsError</span>
<span class="sd">.. autoclass:: TioExportsTimeout</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Optional</span>

<span class="kn">from</span> <span class="nn">restfly.errors</span> <span class="kn">import</span> <span class="o">*</span>  <span class="c1"># noqa:  F403</span>


<div class="viewcode-block" id="AuthenticationWarning"><a class="viewcode-back" href="../../README.md#tenable.errors.AuthenticationWarning">[docs]</a><span class="k">class</span> <span class="nc">AuthenticationWarning</span><span class="p">(</span><span class="ne">Warning</span><span class="p">):</span>  <span class="c1"># noqa: PLW0622</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    An authentication warning is thrown when an unauthenticated API session is</span>
<span class="sd">    initiated.</span>
<span class="sd">    &#39;&#39;&#39;</span></div>


<div class="viewcode-block" id="FileDownloadError"><a class="viewcode-back" href="../../README.md#tenable.errors.FileDownloadError">[docs]</a><span class="k">class</span> <span class="nc">FileDownloadError</span><span class="p">(</span><span class="n">RestflyException</span><span class="p">):</span>  <span class="c1"># noqa:  F405</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    FileDownloadError is thrown when a file fails to download.</span>

<span class="sd">    Attributes:</span>
<span class="sd">        msg (str):</span>
<span class="sd">            The error message</span>
<span class="sd">        filename (str):</span>
<span class="sd">            The Filename or file id that was requested.</span>
<span class="sd">        resource (str):</span>
<span class="sd">            The resource that the file was requested from (e.g. &quot;scans&quot;)</span>
<span class="sd">        resource_id (str):</span>
<span class="sd">            The identifier for the resource that was requested.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">resource</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">resource_id</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">filename</span><span class="p">:</span> <span class="nb">str</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">resource</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">resource</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">resource_id</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">resource_id</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">filename</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">filename</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">msg</span> <span class="o">=</span> <span class="p">(</span>
            <span class="sa">f</span><span class="s1">&#39;resource </span><span class="si">{</span><span class="n">resource</span><span class="si">}</span><span class="s1">:</span><span class="si">{</span><span class="n">resource_id</span><span class="si">}</span><span class="s1"> &#39;</span>
            <span class="sa">f</span><span class="s1">&#39;requested file </span><span class="si">{</span><span class="n">filename</span><span class="si">}</span><span class="s1"> and has failed.&#39;</span>
        <span class="p">)</span></div>


<div class="viewcode-block" id="TioExportsError"><a class="viewcode-back" href="../../README.md#tenable.errors.TioExportsError">[docs]</a><span class="k">class</span> <span class="nc">TioExportsError</span><span class="p">(</span><span class="n">RestflyException</span><span class="p">):</span>  <span class="c1"># noqa:  F405</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    When the exports APIs throw an error when processing an export, pyTenable</span>
<span class="sd">    will throw this error in turn to relay that context to the user.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">export</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">uuid</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">msg</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">export</span> <span class="o">=</span> <span class="n">export</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">uuid</span> <span class="o">=</span> <span class="n">uuid</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">msg</span><span class="p">:</span>
            <span class="n">msg</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">export</span><span class="si">}</span><span class="s1"> export </span><span class="si">{</span><span class="n">uuid</span><span class="si">}</span><span class="s1"> has errored.&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">msg</span> <span class="o">=</span> <span class="n">msg</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">msg</span><span class="p">)</span></div>


<div class="viewcode-block" id="TioExportsTimeout"><a class="viewcode-back" href="../../README.md#tenable.errors.TioExportsTimeout">[docs]</a><span class="k">class</span> <span class="nc">TioExportsTimeout</span><span class="p">(</span><span class="n">TioExportsError</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    When an export has been cancelled due to timeout, this error is thrown.</span>
<span class="sd">    &#39;&#39;&#39;</span>

    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">export</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">uuid</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span> <span class="n">msg</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="nb">str</span><span class="p">]</span> <span class="o">=</span> <span class="kc">None</span><span class="p">):</span>
        <span class="n">msg</span> <span class="o">=</span> <span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">export</span><span class="si">}</span><span class="s1"> export </span><span class="si">{</span><span class="n">uuid</span><span class="si">}</span><span class="s1"> has timed out.&#39;</span>
        <span class="nb">super</span><span class="p">()</span><span class="o">.</span><span class="fm">__init__</span><span class="p">(</span><span class="n">export</span><span class="p">,</span> <span class="n">uuid</span><span class="p">,</span> <span class="n">msg</span><span class="p">)</span></div>


<div class="viewcode-block" id="ImpersonationError"><a class="viewcode-back" href="../../README.md#tenable.errors.ImpersonationError">[docs]</a><span class="k">class</span> <span class="nc">ImpersonationError</span><span class="p">(</span><span class="n">APIError</span><span class="p">):</span>  <span class="c1"># noqa:  F405</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    An ImpersonationError exists when there is an issue with user</span>
<span class="sd">    impersonation.</span>

<span class="sd">    Attributes:</span>
<span class="sd">        code (int):</span>
<span class="sd">            The HTTP response code from the offending response.</span>
<span class="sd">        response (requests.Response):</span>
<span class="sd">            This is the Response object that had caused the Exception to fire.</span>
<span class="sd">        uuid (str):</span>
<span class="sd">            The Request UUID of the request.  This can be used for the purpose</span>
<span class="sd">            of tracking the request and the response through the Tenable.io</span>
<span class="sd">            infrastructure.  In the case of Non-Tenable.io products, is simply</span>
<span class="sd">            an empty string.</span>
<span class="sd">    &#39;&#39;&#39;</span></div>


<div class="viewcode-block" id="PasswordComplexityError"><a class="viewcode-back" href="../../README.md#tenable.errors.PasswordComplexityError">[docs]</a><span class="k">class</span> <span class="nc">PasswordComplexityError</span><span class="p">(</span><span class="n">APIError</span><span class="p">):</span>  <span class="c1"># noqa:  F405</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    PasswordComplexityError is thrown when attempting to change a password and</span>
<span class="sd">    the password complexity is insufficient.</span>

<span class="sd">    Attributes:</span>
<span class="sd">        code (int):</span>
<span class="sd">            The HTTP response code from the offending response.</span>
<span class="sd">        response (requests.Response):</span>
<span class="sd">            This is the Response object that had caused the Exception to fire.</span>
<span class="sd">        uuid (str):</span>
<span class="sd">            The Request UUID of the request.  This can be used for the purpose</span>
<span class="sd">            of tracking the request and the response through the Tenable.io</span>
<span class="sd">            infrastructure.  In the case of Non-Tenable.io products, is simply</span>
<span class="sd">            an empty string.</span>
<span class="sd">    &#39;&#39;&#39;</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.errors</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
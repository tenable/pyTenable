<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../../genindex.md" />
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.lockout_policy.api</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.lockout_policy.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Lockout Policy</span>
<span class="sd">=============</span>
<span class="sd">Methods described in this section relate to the lockout policy API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.lockout_policy``.</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: LockoutPolicyAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">.schema</span> <span class="kn">import</span> <span class="n">LockoutPolicySchema</span>
<div class="viewcode-block" id="LockoutPolicyAPI"><a class="viewcode-back" href="../../../../tenable.ad.lockout_policy.md#tenable.ad.lockout_policy.api.LockoutPolicyAPI">[docs]</a><span class="k">class</span> <span class="nc">LockoutPolicyAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;lockout-policy&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">LockoutPolicySchema</span><span class="p">()</span>
<div class="viewcode-block" id="LockoutPolicyAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.lockout_policy.md#tenable.ad.lockout_policy.api.LockoutPolicyAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Get the lockout policy</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The lockout policy object</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.lockout_policy.details()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">())</span></div>
<div class="viewcode-block" id="LockoutPolicyAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.lockout_policy.md#tenable.ad.lockout_policy.api.LockoutPolicyAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span>
               <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Update the lockout policy</span>
<span class="sd">        Args:</span>
<span class="sd">            enabled (optional, bool):</span>
<span class="sd">                Whether the lockout policy enabled?</span>
<span class="sd">            lockout_duration (optional, int):</span>
<span class="sd">                The time duration for which user will be locked out after</span>
<span class="sd">                several failed login attempts.</span>
<span class="sd">            failed_attempt_threshold (optional, int):</span>
<span class="sd">                The number of failed login attempts to trigger lockout.</span>
<span class="sd">            failed_attempt_period (optional, int):</span>
<span class="sd">                The time to wait before the login attempts count is reseted.</span>
<span class="sd">        Return:</span>
<span class="sd">            None</span>
<span class="sd">        Example:</span>
<span class="sd">            &gt;&gt;&gt; tad.lockout_policy.update(enabled=True)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="n">kwargs</span><span class="p">))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.lockout_policy.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
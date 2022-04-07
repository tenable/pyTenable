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
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" accesskey="U">tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.current</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.current</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Current Session</span>
<span class="sd">===============</span>
<span class="sd">The following methods allow for interaction with the Tenable.sc</span>
<span class="sd">:sc-api:`CurrentOrganization &lt;Current-Organization.html&gt;` API and the</span>
<span class="sd">:sc-api:`CurrentUser &lt;&gt;` API.</span>
<span class="sd">Methods available on ``sc.current``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: CurrentSessionAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="CurrentSessionAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.current.CurrentSessionAPI">[docs]</a><span class="k">class</span> <span class="nc">CurrentSessionAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
<div class="viewcode-block" id="CurrentSessionAPI.associate_cert"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.current.CurrentSessionAPI.associate_cert">[docs]</a>    <span class="k">def</span> <span class="nf">associate_cert</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Associates the certificate passed to the server with the current user&#39;s</span>
<span class="sd">        account.  This allows for authentication via certificate in subsequent</span>
<span class="sd">        logins.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated user record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.current.associate_cert()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;currentUser/associateCert&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CurrentSessionAPI.org"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.current.CurrentSessionAPI.org">[docs]</a>    <span class="k">def</span> <span class="nf">org</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the organization of the current session.</span>
<span class="sd">        :sc-api:`current-organization &lt;Current-Organization.html&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the organization list API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The organization record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; org = sc.current.org()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;currentOrganization&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="CurrentSessionAPI.user"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.current.CurrentSessionAPI.user">[docs]</a>    <span class="k">def</span> <span class="nf">user</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the user of the current session.</span>
<span class="sd">        :sc-api:`current-user &lt;/Current-User.html&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                The list of fields that are desired to be returned.  For details</span>
<span class="sd">                on what fields are available, please refer to the details on the</span>
<span class="sd">                request within the organization list API doc.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The user record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; user = sc.current.user()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;currentUser&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
          <li class="nav-item nav-item-2"><a href="../sc.md" >tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.current</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
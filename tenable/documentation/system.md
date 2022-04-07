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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.system</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.system</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">System</span>
<span class="sd">======</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`System &lt;System.html&gt;` API.  These API calls are typically used to</span>
<span class="sd">understand timezones, system version, etc.</span>
<span class="sd">Methods available on ``sc.system``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: SystemAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>
<span class="kn">import</span> <span class="nn">time</span>
<div class="viewcode-block" id="SystemAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI">[docs]</a><span class="k">class</span> <span class="nc">SystemAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
<div class="viewcode-block" id="SystemAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves information about the Tenable.sc instance.  This method should</span>
<span class="sd">        only be called before authentication has occurred.  As most of the</span>
<span class="sd">        information within this call already happens upon instantiation, there</span>
<span class="sd">        should be little need to call this manually.</span>
<span class="sd">        :sc-api:&#39;system: get &lt;System.html#system_GET&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The response dictionary</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; info = sc.system.details()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;system&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="SystemAPI.diagnostics"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.diagnostics">[docs]</a>    <span class="k">def</span> <span class="nf">diagnostics</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">task</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">options</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Generates and downloads a diagnostic file for the purpose of</span>
<span class="sd">        troubleshooting an ailing Tenable.sc instance.</span>
<span class="sd">        :sc-api:`system: diagnostics-generate &lt;System.html#SystemRESTReference-/system/diagnostics/generate&gt;`</span>
<span class="sd">        :sc-api:`system: diagnostics-download &lt;System.html#SystemRESTReference-/system/diagnostics/download&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                The file-like object to write the diagnostics file to.  If</span>
<span class="sd">                nothing is specified, a BytesIO object will be returnbed with</span>
<span class="sd">                the file.</span>
<span class="sd">            options (list, optional):</span>
<span class="sd">                If performing a diagnostics generation, then which items</span>
<span class="sd">                should be bundled into the diagnostics file?  Available options</span>
<span class="sd">                are ``all``, ``apacheLog``, ``configuration``, ``dependencies``,</span>
<span class="sd">                ``dirlist``, ``environment``, ``installLog``, ``logs``,</span>
<span class="sd">                ``sanitize``, ``scans``, ``serverConf``, ``setup``, ``sysinfo``,</span>
<span class="sd">                and ``upgradeLog``.  If nothing is specified, it will default to</span>
<span class="sd">                ``[&#39;all&#39;]``.</span>
<span class="sd">            task (str, optional):</span>
<span class="sd">                Which task to perform.  Available options are ``appStatus`` and</span>
<span class="sd">                ``diagnosticsFile``.  If nothing is specified, it will default</span>
<span class="sd">                to ``diagnosticFile``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`FileObject`:</span>
<span class="sd">                A file-like object with the diagnostics file specified.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;diagnostics.tar.gz&#39;, &#39;wb&#39;) as fobj:</span>
<span class="sd">            ...     sc.system.diagnostics(fobj=fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;task&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;task&#39;</span><span class="p">,</span> <span class="n">task</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;diagnosticsFile&#39;</span><span class="p">,</span> <span class="s1">&#39;appStatus&#39;</span><span class="p">],</span>
                <span class="n">default</span><span class="o">=</span><span class="s1">&#39;diagnosticsFile&#39;</span><span class="p">),</span>
        <span class="p">}</span>
        <span class="c1"># The available choices for the options.</span>
        <span class="n">opts</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;all&#39;</span><span class="p">,</span> <span class="s1">&#39;apacheLog&#39;</span><span class="p">,</span> <span class="s1">&#39;configuration&#39;</span><span class="p">,</span> <span class="s1">&#39;dependencies&#39;</span><span class="p">,</span>
            <span class="s1">&#39;dirlist&#39;</span><span class="p">,</span> <span class="s1">&#39;environment&#39;</span><span class="p">,</span> <span class="s1">&#39;installLog&#39;</span><span class="p">,</span> <span class="s1">&#39;logs&#39;</span><span class="p">,</span> <span class="s1">&#39;sanitize&#39;</span><span class="p">,</span> <span class="s1">&#39;scans&#39;</span><span class="p">,</span>
            <span class="s1">&#39;serverConf&#39;</span><span class="p">,</span> <span class="s1">&#39;setup&#39;</span><span class="p">,</span> <span class="s1">&#39;sysinfo&#39;</span><span class="p">]</span>
        <span class="c1"># we only want to add the options to the generation call if the task is</span>
        <span class="c1"># a diagnostics file.</span>
        <span class="k">if</span> <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;task&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;diagnosticsFile&#39;</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;options&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;option:item&#39;</span><span class="p">,</span> <span class="n">o</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">opts</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">o</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;options&#39;</span><span class="p">,</span> <span class="n">options</span><span class="p">,</span> <span class="nb">list</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;all&#39;</span><span class="p">])]</span>
        <span class="n">status</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">status</span><span class="p">()</span>
        <span class="c1"># Make the call to generate the disagnostics file.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;system/diagnostics/generate&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span>
        <span class="c1"># We will sleep until the file has been generated.  We will know when</span>
        <span class="c1"># the file is ready or download as the `diagnosticsGenerated` timestamp</span>
        <span class="c1"># will have been updated.</span>
        <span class="k">while</span> <span class="bp">self</span><span class="o">.</span><span class="n">status</span><span class="p">()[</span><span class="s1">&#39;diagnosticsGenerated&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="n">status</span><span class="p">[</span><span class="s1">&#39;diagnosticsGenerated&#39;</span><span class="p">]:</span>
            <span class="n">time</span><span class="o">.</span><span class="n">sleep</span><span class="p">(</span><span class="mi">5</span><span class="p">)</span>
        <span class="c1"># Make the call to download the file.</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;system/diagnostics/download&#39;</span><span class="p">,</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="c1"># if no file-like object was passed, then we will instantiate a BytesIO</span>
        <span class="c1"># object to push the file into.</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">fobj</span><span class="p">:</span>
            <span class="n">fobj</span> <span class="o">=</span> <span class="n">BytesIO</span><span class="p">()</span>
        <span class="c1"># Lets stream the file into the file-like object...</span>
        <span class="k">for</span> <span class="n">chunk</span> <span class="ow">in</span> <span class="n">resp</span><span class="o">.</span><span class="n">iter_content</span><span class="p">(</span><span class="n">chunk_size</span><span class="o">=</span><span class="mi">1024</span><span class="p">):</span>
            <span class="k">if</span> <span class="n">chunk</span><span class="p">:</span>
                <span class="n">fobj</span><span class="o">.</span><span class="n">write</span><span class="p">(</span><span class="n">chunk</span><span class="p">)</span>
        <span class="n">fobj</span><span class="o">.</span><span class="n">seek</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span>
        <span class="n">resp</span><span class="o">.</span><span class="n">close</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">fobj</span></div>
<div class="viewcode-block" id="SystemAPI.current_locale"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.current_locale">[docs]</a>    <span class="k">def</span> <span class="nf">current_locale</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the current system locale that Tenable.sc has been set to.</span>
<span class="sd">        :sc-api:`system: locale &lt;System.html#SystemRESTReference-/system/locale&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                locale resource</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.system.current_locale()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;system/locale&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="SystemAPI.list_locales"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.list_locales">[docs]</a>    <span class="k">def</span> <span class="nf">list_locales</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the available system locales that Tenable.sc can be set to.</span>
<span class="sd">        :sc-api:`system: locales &lt;System.html#SystemRESTReference-/system/locales&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                locales dictionary</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.system.list_locales()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;system/locales&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="SystemAPI.set_locale"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.set_locale">[docs]</a>    <span class="k">def</span> <span class="nf">set_locale</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">locale</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Sets the system locale to be used.  This requires an administrator to</span>
<span class="sd">        perform this task and will be a global change.  The locale determines</span>
<span class="sd">        which pluginset language to use.</span>
<span class="sd">        :sc-api:`system: set-locale &lt;System.html#system_locale_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            locale (str): The plugin locale name</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                The new plugin locale.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Set the system locale to Japanese:</span>
<span class="sd">            &gt;&gt;&gt; sc.system.set_locale(&#39;ja&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;system/locale&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;PluginLocale&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;locale&#39;</span><span class="p">,</span> <span class="n">locale</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
            <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="SystemAPI.status"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.system.SystemAPI.status">[docs]</a>    <span class="k">def</span> <span class="nf">status</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the current system status</span>
<span class="sd">        :sc-api:`system: diagnostics &lt;System.html#SystemRESTReference-/system/diagnostics&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The status dictionary</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; status = sc.system.status()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;system/diagnostics&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.system</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
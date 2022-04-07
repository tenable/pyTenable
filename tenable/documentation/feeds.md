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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.feeds</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.feeds</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Feeds</span>
<span class="sd">=====</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Feed &lt;Feed.html&gt;` API.</span>
<span class="sd">Methods available on ``sc.feeds``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: FeedAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="FeedAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.feeds.FeedAPI">[docs]</a><span class="k">class</span> <span class="nc">FeedAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
<div class="viewcode-block" id="FeedAPI.status"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.feeds.FeedAPI.status">[docs]</a>    <span class="k">def</span> <span class="nf">status</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">feed_type</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the status of either a specific feed type (if requested) or all</span>
<span class="sd">        of the feed types if nothing is specifically asked.</span>
<span class="sd">        :sc-api:`feed &lt;Feed.html&gt;`</span>
<span class="sd">        :sc-api:`feed: feed-type &lt;Feed.html#FeedRESTReference-FeedGETType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            feed_type (str, optional):</span>
<span class="sd">                The feed type to specifically return.  Valid types are `active`,</span>
<span class="sd">                `passive`, `lce`, `sc`, or `all`.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                If no specific feed type is specified, then a dictionary with</span>
<span class="sd">                each type listed with a sub-dictionary detailing the status is</span>
<span class="sd">                returned.  If a specific feed type is requested, then only the</span>
<span class="sd">                status information for that feed type is returned.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Getting all of the feed types returned:</span>
<span class="sd">            &gt;&gt;&gt; status = sc.feed.status()</span>
<span class="sd">            Getting the feed status for a specific type (e.g. `active`).</span>
<span class="sd">            &gt;&gt;&gt; status = sc.feeds.status(&#39;active&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;feed_type&#39;</span><span class="p">,</span> <span class="n">feed_type</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
            <span class="s1">&#39;active&#39;</span><span class="p">,</span> <span class="s1">&#39;passive&#39;</span><span class="p">,</span> <span class="s1">&#39;lce&#39;</span><span class="p">,</span> <span class="s1">&#39;sc&#39;</span><span class="p">,</span> <span class="s1">&#39;all&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="ow">not</span> <span class="n">feed_type</span><span class="p">:</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;feed&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;feed/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">feed_type</span><span class="p">))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="FeedAPI.update"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.feeds.FeedAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">feed_type</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Initiates an on-line feed update based on the specified feed_type.  If</span>
<span class="sd">        no feed type is specified, then it will default to initiating an update</span>
<span class="sd">        for all feed types.</span>
<span class="sd">        :sc-api:`feed: update &lt;Feed.html#FeedRESTReference-FeedUpdatePOSTType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            feed_type (str, optional);</span>
<span class="sd">                The feed type to specifically return.  Valid types are `active`,</span>
<span class="sd">                `passive`, `lce`, `sc`, or `all`.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`None`: Update successfully requested.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;feed/</span><span class="si">{}</span><span class="s1">/update&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;feed_type&#39;</span><span class="p">,</span> <span class="n">feed_type</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;all&#39;</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;active&#39;</span><span class="p">,</span> <span class="s1">&#39;passive&#39;</span><span class="p">,</span> <span class="s1">&#39;lce&#39;</span><span class="p">,</span> <span class="s1">&#39;sc&#39;</span><span class="p">,</span> <span class="s1">&#39;all&#39;</span><span class="p">])),</span> <span class="n">json</span><span class="o">=</span><span class="p">{})</span></div>
<div class="viewcode-block" id="FeedAPI.process"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.feeds.FeedAPI.process">[docs]</a>    <span class="k">def</span> <span class="nf">process</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">feed_type</span><span class="p">,</span> <span class="n">fobj</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Initiates an off-line feed update based on the specified feed_type using</span>
<span class="sd">        the file object passed as the update file.</span>
<span class="sd">        :sc-api:`feed: process &lt;Feed.html#FeedRESTReference-FeedUpdatePOSTProcess&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            feed_type (str);</span>
<span class="sd">                The feed type to specifically return.  Valid types are `active`,</span>
<span class="sd">                `passive`, `lce`, `sc`, or `all`.</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file object to upload into SecurityCenter and use as the</span>
<span class="sd">                update package.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`None`:</span>
<span class="sd">                Update successfully requested.</span>
<span class="sd">        Examples:</span>
<span class="sd">            updating the active plugins:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;sc-plugins-diff.tar.gz&#39;, &#39;rb&#39;) as plugfile:</span>
<span class="sd">            ...     sc.feeds.process(&#39;active&#39;, plugfile)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">filename</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">fobj</span><span class="p">)</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;feed/</span><span class="si">{}</span><span class="s1">/process&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;feed_type&#39;</span><span class="p">,</span> <span class="n">feed_type</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;active&#39;</span><span class="p">,</span> <span class="s1">&#39;passive&#39;</span><span class="p">,</span> <span class="s1">&#39;lce&#39;</span><span class="p">,</span> <span class="s1">&#39;sc&#39;</span><span class="p">])),</span>
            <span class="n">json</span><span class="o">=</span><span class="p">{</span><span class="s1">&#39;filename&#39;</span><span class="p">:</span> <span class="n">filename</span><span class="p">})</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.feeds</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
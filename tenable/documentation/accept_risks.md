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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.accept_risks</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.accept_risks</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Accept Risks</span>
<span class="sd">============</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Accept Risk &lt;Accept-Risk-Rule.html&gt;` API.</span>
<span class="sd">Methods available on ``sc.accept_risks``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AcceptRiskAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<div class="viewcode-block" id="AcceptRiskAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI">[docs]</a><span class="k">class</span> <span class="nc">AcceptRiskAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        document creator for acceptRisk creation and update calls.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;repos&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># as repositories are passed in the API as a series of sub-documents</span>
            <span class="c1"># with the ID attribute set, we will convert the simply list that</span>
            <span class="c1"># was passed to us into a series of documents as the API expects.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repositories&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">r</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repos&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repos&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repos&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;plugin_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># the plugin parameter</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
                <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># as the port will only be passed if the default of &quot;any&quot; isn&#39;t</span>
            <span class="c1"># desired, we should check to make sure that the value passed is an</span>
            <span class="c1"># integer, and then convert it into a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;protocol&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># as the protocol will only be passed if the default of &quot;any&quot; isn&#39;t</span>
            <span class="c1"># desired, we should check to make sure that the value passed is an</span>
            <span class="c1"># integer, and then convert it into a string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;protocol&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;protocol&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;protocol&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
        <span class="k">if</span> <span class="s1">&#39;comments&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if a comment is attached to the rule, then lets just make sure</span>
            <span class="c1"># that we actually have a string here before moving on.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;comments&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;comments&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;expires&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># how many days until the accept risk rule expires?  We should</span>
            <span class="c1"># simply checkt o see if the value is an integer.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;expires&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;expires&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;ips&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if the ips list is passed, then</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;ip&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostValue&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ip:item&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ips&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;uuids&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;uuid&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostValue&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;uuid:item&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;uuids&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;uuids&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;uuids&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;asset_list&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;asset&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostValue&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;asset_list&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;asset_list&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;asset_list&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="AcceptRiskAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">repo_ids</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">plugin_id</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">port</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span>
             <span class="n">org_ids</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of accepted risk rules.</span>
<span class="sd">        :sc-api:`accept-risk: list &lt;Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each accepted risk rule.</span>
<span class="sd">            plugin_id (int, optional):</span>
<span class="sd">                Plugin id to filter the response on.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                Port number to filter the response on.</span>
<span class="sd">            org_ids (list, optional):</span>
<span class="sd">                List of organization ids to filter on.</span>
<span class="sd">            repo_ids (list, optional):</span>
<span class="sd">                List of repository ids to filter the response on.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of accepted risk rules.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for rule in sc.accept_risks.list():</span>
<span class="sd">            ...     pprint(rule)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">if</span> <span class="n">plugin_id</span><span class="p">:</span>
            <span class="c1"># validating that the plugin_id is an integer and assigning it to</span>
            <span class="c1"># the appropriate query parameter.</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;pluginID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">port</span><span class="p">:</span>
            <span class="c1"># validating that port is an integer and assigning it to the</span>
            <span class="c1"># appropriate query parameter.</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">port</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">org_ids</span><span class="p">:</span>
            <span class="c1"># validating that org_ids is a list of integer values, then</span>
            <span class="c1"># converting the result into a comma-seperated string and assigning</span>
            <span class="c1"># it to the appropriate query parameter.</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;organizationIDs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">))</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_ids&#39;</span><span class="p">,</span> <span class="n">org_ids</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">if</span> <span class="n">repo_ids</span><span class="p">:</span>
            <span class="c1"># validating that repo_ids is a list of integer values, then</span>
            <span class="c1"># converting the result into a comma-seperated string and assigning</span>
            <span class="c1"># it to the appropriate query parameter.</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;repositoryIDs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">))</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo_ids&#39;</span><span class="p">,</span> <span class="n">repo_ids</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;acceptRiskRule&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AcceptRiskAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details of an accepted risk rule.</span>
<span class="sd">        :sc-api:`accept-riskL details &lt;Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule/{id}&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the accept risk rule.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each accepted risk rule.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The accept risk rule details.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; rule = sc.accept_risks.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(rule)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;acceptRiskRule/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AcceptRiskAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the accepted risk rule from Tenable.sc</span>
<span class="sd">        :sc-api:`accept-risk: delete &lt;Accept-Risk-Rule.html#acceptRiskRule_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the accept risk rule.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty string response from the API.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.accept_risks.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;acceptRiskRule/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AcceptRiskAPI.apply"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI.apply">[docs]</a>    <span class="k">def</span> <span class="nf">apply</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">repo</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Applies the accept risk rule for either all repositories, or the</span>
<span class="sd">        repository specified.</span>
<span class="sd">        :sc-api:`accept-risk: apply &lt;Accept-Risk-Rule.html#AcceptRiskRuleRESTReference-/acceptRiskRule/apply&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the accept risk rule.</span>
<span class="sd">            repo (int, optional):</span>
<span class="sd">                A specific repository to apply the rule to.  The default if not</span>
<span class="sd">                specified is all repositories (``0``).</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty string response from the API.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.accept_risks.apply(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;acceptRiskRule/</span><span class="si">{}</span><span class="s1">/apply&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;repository&#39;</span><span class="p">:</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo&#39;</span><span class="p">,</span> <span class="n">repo</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AcceptRiskAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.accept_risks.AcceptRiskAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="n">repos</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new accept risk rule.  Either ips, uuids, or asset_list must</span>
<span class="sd">        be specified.</span>
<span class="sd">        :sc-api:`accept-risk: create &lt;Accept-Risk-Rule.html#acceptRiskRule_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            plugin_id (int): The plugin to apply the accept risk rule to.</span>
<span class="sd">            repos (list):</span>
<span class="sd">                The list of repositories to apply this accept risk rule to.</span>
<span class="sd">            asset_list (int, optional):</span>
<span class="sd">                The asset list id to apply the accept risk rule to.  Please note</span>
<span class="sd">                that ``asset_list``, ``ips``, and ``uuids`` are mutually</span>
<span class="sd">                exclusive.</span>
<span class="sd">            comments (str, optional):</span>
<span class="sd">                The comment associated to the accept risk rule.</span>
<span class="sd">            expires (int, optional):</span>
<span class="sd">                Timestamp. When should the rule expire?  if no expiration is set, the rule</span>
<span class="sd">                will never expire. If not mentioned, value is -1</span>
<span class="sd">                (-1 represents December 31st 1969 23:59:59 hours GMT)</span>
<span class="sd">            ips (list, optional):</span>
<span class="sd">                A list of IPs to apply the accept risk rule to.  Please note</span>
<span class="sd">                that ``asset_list``, ``ips``, and ``uuids`` are mutually</span>
<span class="sd">                exclusive.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                The port to restrict this accept risk rule to.  The default is</span>
<span class="sd">                unrestricted.</span>
<span class="sd">            protocol (int, optional):</span>
<span class="sd">                The protocol to restrict the accept risk rule to.  The default</span>
<span class="sd">                is unrestricted.</span>
<span class="sd">            uuids (list, optional):</span>
<span class="sd">                The agent uuids to apply the accept risk rule to.  Please note</span>
<span class="sd">                that ``asset_list``, ``ips``, and ``uuids`` are mutually</span>
<span class="sd">                exclusive.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created accept risk rule definition.</span>
<span class="sd">        Examples:</span>
<span class="sd">            Create a rule to accept 97737 on 2 IPs till Aug 25th 2021 00:00 Hrs GMT.</span>
<span class="sd">            &gt;&gt;&gt; rule = sc.accept_risks.create(97737, [1],</span>
<span class="sd">            ...     ips=[&#39;192.168.0.101&#39;, &#39;192.168.0.102&#39;], expires=1629849600)</span>
<span class="sd">            Create a rule to accept 97737 on all IPs on repository 1:</span>
<span class="sd">            &gt;&gt;&gt; rule = sc.accept_risks.create(97737, [1])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;hostType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;all&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">plugin_id</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repos&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">repos</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;acceptRiskRule&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="mi">0</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.accept_risks</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.analysis</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.analysis</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Analysis</span>
<span class="sd">========</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`analysis &lt;Analysis.html&gt;` API.  The analysis area in Tenable.sc is</span>
<span class="sd">highly complex and allows for a wide range of varied inputs and outputs.  This</span>
<span class="sd">single endpoint has been broken down in pyTenable to several methods in order to</span>
<span class="sd">apply some defaults to the expected data-types and options most likely to be</span>
<span class="sd">returned.  As the filters are dependent on the tool and data-type that is being</span>
<span class="sd">referenced, the best solution to understanding what filters are available when</span>
<span class="sd">getting started is to simply pass a known bad filter string and use the</span>
<span class="sd">resulting error as an indicator of what&#39;s available.  For example, you could</span>
<span class="sd">perform the following action below while attempting to see the available filters</span>
<span class="sd">for the mobile data-type when using the ``vulndetails`` tool:</span>
<span class="sd">.. code-block:: python</span>
<span class="sd">    &gt;&gt;&gt; x = sc.analysis.mobile((&#39;something&#39;, &#39;=&#39;, &#39;&#39;))</span>
<span class="sd">    &gt;&gt;&gt; x.next()</span>
<span class="sd">    Traceback (most recent call last):</span>
<span class="sd">      File &quot;&lt;input&gt;&quot;, line 1, in &lt;module&gt;</span>
<span class="sd">        x.next()</span>
<span class="sd">      File &quot;tenable/base.py&quot;, line 75, in next</span>
<span class="sd">        self._get_page()</span>
<span class="sd">      File &quot;tenable/sc/analysis.py&quot;, line 43, in _get_page</span>
<span class="sd">      File &quot;tenable/base.py&quot;, line 436, in post</span>
<span class="sd">        return self._request(&#39;POST&#39;, path, **kwargs)</span>
<span class="sd">      File &quot;tenable/base.py&quot;, line 379, in _request</span>
<span class="sd">        raise self._error_codes[status](resp)</span>
<span class="sd">    ForbiddenError: 00000000-0000-0000-0000-000000000000:403 {&quot;type&quot;:&quot;regular&quot;,</span>
<span class="sd">    &quot;response&quot;:&quot;&quot;,&quot;error_code&quot;:146,&quot;error_msg&quot;:&quot;Invalid parameters specified for</span>
<span class="sd">    mobile vuln query.  The filter &#39;something&#39; is invalid (valid filters:</span>
<span class="sd">    repositoryIDs, port, pluginID, familyID, pluginOutput, lastSeen,</span>
<span class="sd">    lastMitigated, severity, protocol, pluginName, baseCVSSScore,</span>
<span class="sd">    exploitAvailable, pluginPublished, pluginModified, vulnPublished,</span>
<span class="sd">    patchPublished, deviceID, mdmType, deviceModel, serialNumber, deviceUser,</span>
<span class="sd">    deviceVersion, osCPE).&quot;,&quot;warnings&quot;:[],&quot;timestamp&quot;:1545060739}</span>
<span class="sd">The resulting error details specifically what filters can be set.</span>
<span class="sd">When it comes to constructing filters, TenableSC uses a common filter structure</span>
<span class="sd">for the collapsed filter-set.  This format is in the form of a 3 entry tuple</span>
<span class="sd">consisting of (&#39;filtername&#39;, &#39;operator&#39;, &#39;value&#39;).  For example, if you&#39;re</span>
<span class="sd">looking to set the ``pluginID`` filter to ``19506`` the filter would look like</span>
<span class="sd">``(&#39;pluginID&#39;, &#39;=&#39;, &#39;19506&#39;)``.  Severities are in level of criticality, from 0</span>
<span class="sd">(informational) to 4 (critical).  Filters like these can be a string of comma-</span>
<span class="sd">separated values to indicate multiple items.  So for high and critical vulns,</span>
<span class="sd">``(&#39;severity&#39;, &#39;=&#39;, &#39;3,4&#39;)`` would return only what your looking for.</span>
<span class="sd">Asset list calculations in filters are a bit more complex, but still shouldn&#39;t</span>
<span class="sd">be too difficult.  Tenable.sc leverages nested pairs for the asset calculations</span>
<span class="sd">combined with a operator to define how that pair are to be combined.  Each of</span>
<span class="sd">the elements within the pair can further be nested, allowing for some quite</span>
<span class="sd">complex asset list math to happen.</span>
<span class="sd">On the simple side, if you just want to look for The the combined results of</span>
<span class="sd">asset lists 1 or 2, you would perform:</span>
<span class="sd">``(&#39;asset&#39;, &#39;~&#39;, (&#39;or&#39;, 1, 2))``.</span>
<span class="sd">Note the tilda, informing the filtering engine that it will need to perform some</span>
<span class="sd">sort of calculation first.  The tilda is only used when using the asset filter.</span>
<span class="sd">Now for a more complex calculation, you could look for the IPs that exist in</span>
<span class="sd">both 1 or 2, but not 3:</span>
<span class="sd">``(&#39;asset&#39;, &#39;~&#39;, (&#39;and&#39;, (&#39;or&#39;, 1, 2), (&#39;not&#39;, 3)))``</span>
<span class="sd">As you can see it&#39;s just a matter of nesting out from &quot;1 or 2&quot;.  The only new</span>
<span class="sd">concept here is the paired tuple for not.  asking for the inverse of an asset</span>
<span class="sd">list requires that you wrap it in a tuple with the not operator.</span>
<span class="sd">Methods available on ``sc.analysis``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AnalysisAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span><span class="p">,</span> <span class="n">SCResultsIterator</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">UnexpectedValueError</span>
<div class="viewcode-block" id="AnalysisResultsIterator"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisResultsIterator">[docs]</a><span class="k">class</span> <span class="nc">AnalysisResultsIterator</span><span class="p">(</span><span class="n">SCResultsIterator</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_get_page</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the next page of results when the current page has been</span>
<span class="sd">        exhausted.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># First we need to see if there is a page limit and if there is, have</span>
        <span class="c1"># we run into that limit.  If we have, then return a StopIteration</span>
        <span class="c1"># exception.</span>
        <span class="k">if</span> <span class="bp">self</span><span class="o">.</span><span class="n">_pages_total</span> <span class="ow">and</span> <span class="bp">self</span><span class="o">.</span><span class="n">_pages_requested</span> <span class="o">&gt;=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_pages_total</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">StopIteration</span><span class="p">()</span>
        <span class="c1"># Now we need to do is construct the query with the current offset</span>
        <span class="c1"># and limits</span>
        <span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query</span>
        <span class="n">query</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span>
        <span class="n">query</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span>
        <span class="c1"># Lets actually call the API for the data at this point.</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;analysis&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">query</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()</span>
        <span class="c1"># Now that we have the response, lets reset any counters we need to,</span>
        <span class="c1"># and increment things like the page counter, offset, etc.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">page_count</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_pages_requested</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span> <span class="o">+=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_raw</span> <span class="o">=</span> <span class="n">resp</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">page</span> <span class="o">=</span> <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;results&#39;</span><span class="p">]</span>
        <span class="c1"># sadly the totalRecords attribute isn&#39;t always returned.  If it is</span>
        <span class="c1"># returned, then we will simply update our total with the value of</span>
        <span class="c1"># totalRecords.  In the absence of a totalRecords, we will simply want</span>
        <span class="c1"># to check to see if the number of records equaled the page limiter.</span>
        <span class="c1"># if it did, then we will assume that there is likely another page</span>
        <span class="c1"># ahead of this one and set the total count to be the limit + count + 1.</span>
        <span class="c1"># If the page size is less than the page limit, then we can likely</span>
        <span class="c1"># assume that this is the last page, and just set the total to be the</span>
        <span class="c1"># count + size of the page.</span>
        <span class="n">total_records</span> <span class="o">=</span> <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;totalRecords&#39;</span><span class="p">)</span>
        <span class="n">records</span> <span class="o">=</span> <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;returnedRecords&#39;</span><span class="p">)</span>
        <span class="n">page_size</span> <span class="o">=</span> <span class="nb">len</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;results&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="n">page_size</span> <span class="o">==</span> <span class="n">records</span> <span class="ow">and</span> <span class="n">total_records</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">total</span> <span class="o">=</span> <span class="nb">int</span><span class="p">(</span><span class="n">total_records</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_log</span><span class="o">.</span><span class="n">warning</span><span class="p">(</span><span class="s1">&#39; &#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span>
                <span class="s1">&#39;API Recordkeeping error.&#39;</span><span class="p">,</span>
                <span class="s1">&#39;api_total=</span><span class="si">{}</span><span class="s1">,&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">total_records</span><span class="p">)),</span>
                <span class="s1">&#39;api_count=</span><span class="si">{}</span><span class="s1">,&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">records</span><span class="p">)),</span>
                <span class="s1">&#39;page_size=</span><span class="si">{}</span><span class="s1">,&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">page_size</span><span class="p">)),</span>
                <span class="s1">&#39;iter_total=</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">total</span><span class="p">))</span>
            <span class="p">]))</span>
            <span class="k">if</span> <span class="n">page_size</span> <span class="o">&lt;</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">total</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">count</span> <span class="o">+</span> <span class="n">page_size</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">total</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">count</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span> <span class="o">+</span> <span class="mi">1</span></div>
<div class="viewcode-block" id="AnalysisAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI">[docs]</a><span class="k">class</span> <span class="nc">AnalysisAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_analysis</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        The base wrapper function handling the calls to the analysis API</span>
<span class="sd">        endpoint.  As this singular endpoint is used as the common API for all</span>
<span class="sd">        data export, much of the common handling can be centrally handled and</span>
<span class="sd">        only the unique elements for a given sub-type is handled by the</span>
<span class="sd">        individual methods.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">offset</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="n">limit</span> <span class="o">=</span> <span class="mi">1000</span>
        <span class="n">pages</span> <span class="o">=</span> <span class="kc">None</span>
        <span class="c1"># Call the query constructor to build the query if necessary./</span>
        <span class="n">kw</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;payload&#39;</span><span class="p">]</span> <span class="k">if</span> <span class="s1">&#39;payload&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="k">else</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="s1">&#39;sort_field&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;sortField&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_field&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;sort_direction&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;sortDir&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_direction&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_direction&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ASC&#39;</span><span class="p">,</span> <span class="s1">&#39;DESC&#39;</span><span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;offset&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">offset</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;offset&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">0</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;limit&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">limit</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;limit&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">,</span> <span class="n">default</span><span class="o">=</span><span class="mi">200</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;pages&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">pages</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;pages&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">payload</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;sourceType&#39;</span><span class="p">)</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;individual&#39;</span><span class="p">]:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;view&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;view&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;view&#39;</span><span class="p">,</span> <span class="s1">&#39;all&#39;</span><span class="p">),</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;all&#39;</span><span class="p">,</span> <span class="s1">&#39;new&#39;</span><span class="p">,</span> <span class="s1">&#39;patched&#39;</span><span class="p">],</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;all&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;json_result&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;json_result&#39;</span><span class="p">]:</span>
            <span class="c1"># if the json_result flag is set, then we do not want to return an</span>
            <span class="c1"># iterator, and instead just want to return the results section of</span>
            <span class="c1"># the response.</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">offset</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">limit</span> <span class="o">+</span> <span class="n">offset</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span>
                <span class="s1">&#39;analysis&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="c1"># the default option is the return the AnalysisResultsIterator</span>
            <span class="k">return</span> <span class="n">AnalysisResultsIterator</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="p">,</span>
                <span class="n">_offset</span><span class="o">=</span><span class="n">offset</span><span class="p">,</span>
                <span class="n">_limit</span><span class="o">=</span><span class="n">limit</span><span class="p">,</span>
                <span class="n">_query</span><span class="o">=</span><span class="n">payload</span><span class="p">,</span>
                <span class="n">_pages_total</span><span class="o">=</span><span class="n">pages</span><span class="p">,</span>
            <span class="p">)</span>
<div class="viewcode-block" id="AnalysisAPI.vulns"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI.vulns">[docs]</a>    <span class="k">def</span> <span class="nf">vulns</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Query&#39;s the analysis API for vulnerability data within the cumulative</span>
<span class="sd">        repositories.</span>
<span class="sd">        :sc-api:`analysis: vuln-type &lt;Analysis.html#AnalysisRESTReference-VulnType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            filters (tuple, optional):</span>
<span class="sd">                The analysis module provides a more compact way to write filters</span>
<span class="sd">                to the analysis endpoint.  The purpose here is to aid in more</span>
<span class="sd">                readable code and reduce the amount of boilerplate that must be</span>
<span class="sd">                written to support a filtered call to analysis.  The format is</span>
<span class="sd">                simply a list of tuples.  Each tuple is broken down into</span>
<span class="sd">                (field, operator, value).</span>
<span class="sd">            query_id (int, optional):</span>
<span class="sd">                The ID number of the SC Query where filters should be pulled from in place of the tuple filters. This is</span>
<span class="sd">                mutually exclusive with the tuple filters.</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                The number of pages to query.  Default is all.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many entries should be in each page?  Default is 200.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                How many entries to skip before processing.  Default is 0.</span>
<span class="sd">            source (str, optional):</span>
<span class="sd">                The data source location.  Allowed sources are ``cumulative``</span>
<span class="sd">                and ``patched``.  Defaults to ``cumulative``.</span>
<span class="sd">            scan_id (int, optional):</span>
<span class="sd">                If a scan id is specified, then the results fetched will be from</span>
<span class="sd">                the scan specified and not from the cumulative result set.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                The analysis tool for formatting and returning a specific view</span>
<span class="sd">                into the information.  If no tool is specified, the default will</span>
<span class="sd">                be ``vulndetails``.  Available tools are:</span>
<span class="sd">                ``cceipdetail``, ``cveipdetail``, ``iavmipdetail``,</span>
<span class="sd">                ``iplist``, ``listmailclients``, ``listservices``,</span>
<span class="sd">                ``listos``, ``listsoftware``, ``listsshservers``,</span>
<span class="sd">                ``listvuln``, ``listwebclients``, ``listwebservers``,</span>
<span class="sd">                ``sumasset``, ``sumcce``, ``sumclassa``, ``sumclassb``,</span>
<span class="sd">                ``sumclassc``, ``sumcve``, ``sumdnsname``,</span>
<span class="sd">                ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,</span>
<span class="sd">                ``summsbulletin``, ``sumprotocol``, ``sumremediation``,</span>
<span class="sd">                ``sumseverity``, ``sumuserresponsibility``, ``sumport``,</span>
<span class="sd">                ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`AnalysisResultsIterator`:</span>
<span class="sd">                An iterator object handling data pagination.</span>
<span class="sd">        Examples:</span>
<span class="sd">            A quick example showing how to get all of the information stored in</span>
<span class="sd">            SecurityCenter.  As the default is for the vulns method to return</span>
<span class="sd">            data from the vulndetails tool, we can handle this without actually</span>
<span class="sd">            doing anything other than calling</span>
<span class="sd">            &gt;&gt;&gt; from pprint import pprint</span>
<span class="sd">            &gt;&gt;&gt; for vuln in sc.analysis.vulns():</span>
<span class="sd">            ...     pprint(vuln)</span>
<span class="sd">            To ask for a specific subset of information (like only critical and</span>
<span class="sd">            exploitable vulns) you&#39;d want to pass the filter tuples into the</span>
<span class="sd">            query like so:</span>
<span class="sd">            &gt;&gt;&gt; vulns = sc.analysis.vulns(</span>
<span class="sd">            ...    (&#39;severity&#39;, &#39;=&#39;, &#39;4&#39;),</span>
<span class="sd">            ...    (&#39;exploitAvailable&#39;, &#39;=&#39;, &#39;true&#39;))</span>
<span class="sd">            To request a different data format (like maybe an IP summary of</span>
<span class="sd">            vulns) you just need to specify the appropriate tool:</span>
<span class="sd">            &gt;&gt;&gt; ips = sc.analysis.vulns(</span>
<span class="sd">            ...    (&#39;severity&#39;, &#39;=&#39;, &#39;4&#39;),</span>
<span class="sd">            ...    (&#39;exploitAvailable&#39;, &#39;=&#39;, &#39;true&#39;), tool=&#39;sumip&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;vuln&#39;</span><span class="p">,</span>
            <span class="s1">&#39;sourceType&#39;</span><span class="p">:</span> <span class="s1">&#39;cumulative&#39;</span><span class="p">,</span>
        <span class="p">}</span>
        <span class="k">if</span> <span class="s1">&#39;source&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;sourceType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;source&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;source&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;cumulative&#39;</span><span class="p">,</span> <span class="s1">&#39;patched&#39;</span><span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;tool&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tool&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;cceipdetail&#39;</span><span class="p">,</span>
                <span class="s1">&#39;cveipdetail&#39;</span><span class="p">,</span>
                <span class="s1">&#39;iavmipdetail&#39;</span><span class="p">,</span>
                <span class="s1">&#39;iplist&#39;</span><span class="p">,</span> <span class="c1"># not sure if this should be removed...</span>
                <span class="s1">&#39;listmailclients&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listservices&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listos&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listsoftware&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listsshservers&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listvuln&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listwebclients&#39;</span><span class="p">,</span>
                <span class="s1">&#39;listwebservers&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumasset&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumcce&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassa&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassb&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassc&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumcve&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumdnsname&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumfamily&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumiavm&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumid&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumip&#39;</span><span class="p">,</span>
                <span class="s1">&#39;summsbulletin&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumport&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumprotocol&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumremediation&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumseverity&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumuserresponsibility&#39;</span><span class="p">,</span>
                <span class="s1">&#39;trend&#39;</span><span class="p">,</span>
                <span class="s1">&#39;vulndetails&#39;</span><span class="p">,</span>
                <span class="s1">&#39;vulnipdetail&#39;</span><span class="p">,</span>
                <span class="s1">&#39;vulnipsummary&#39;</span><span class="p">,</span>
            <span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;vulndetails&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;scan_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;sourceType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;individual&#39;</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;scanID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_id&#39;</span><span class="p">]</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;payload&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">payload</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;vuln&#39;</span>
        <span class="c1"># DIRTYHACK - If the tool is set to &#39;iplist&#39;, then we will want to make</span>
        <span class="c1">#             sure to specify that the json_result flag is set to bypass</span>
        <span class="c1">#             the iterator.  The iplist dataset is instead a dictionary</span>
        <span class="c1">#             and not a list.</span>
        <span class="k">if</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;iplist&#39;</span><span class="p">:</span>
            <span class="c1"># set the json_result flag to True and call the _analysis method.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;json_result&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="kc">True</span>
            <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_analysis</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
            <span class="c1"># The results attribute always appears to be NoneType, so lets</span>
            <span class="c1"># remove it in the interest of trying to keep a clean return.</span>
            <span class="k">del</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;results&#39;</span><span class="p">])</span>
            <span class="k">return</span> <span class="n">resp</span>
        <span class="c1"># call the _analysis method and return the results to the caller.</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_analysis</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span></div>
<div class="viewcode-block" id="AnalysisAPI.scan"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI.scan">[docs]</a>    <span class="k">def</span> <span class="nf">scan</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">scan_id</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Queries the analysis API for vulnerability data from a specific scan.</span>
<span class="sd">        :sc-api:`analysis: vuln-type &lt;Analysis.html#AnalysisRESTReference-VulnType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            scan_id (int):</span>
<span class="sd">                If a scan id is specified, then the results fetched will be from</span>
<span class="sd">                the scan specified and not from the cumulative result set.</span>
<span class="sd">            filters (tuple, optional):</span>
<span class="sd">                The analysis module provides a more compact way to write filters</span>
<span class="sd">                to the analysis endpoint.  The purpose here is to aid in more</span>
<span class="sd">                readable code and reduce the amount of boilerplate that must be</span>
<span class="sd">                written to support a filtered call to analysis.  The format is</span>
<span class="sd">                simply a list of tuples.  Each tuple is broken down into</span>
<span class="sd">                (field, operator, value).</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                The number of pages to query.  Default is all.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many entries should be in each page?  Default is 200.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                How many entries to skip before processing.  Default is 0.</span>
<span class="sd">            source (str, optional):</span>
<span class="sd">                The data source location.  Allowed sources are ``cumulative``</span>
<span class="sd">                and ``patched``.  Defaults to ``cumulative``.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                The analysis tool for formatting and returning a specific view</span>
<span class="sd">                into the information.  If no tool is specified, the default will</span>
<span class="sd">                be ``vulndetails``.  Available tools are:</span>
<span class="sd">                ``cceipdetail``, ``cveipdetail``, ``iavmipdetail``,</span>
<span class="sd">                ``iplist``, ``listmailclients``, ``listservices``,</span>
<span class="sd">                ``listos``, ``listsoftware``, ``listsshservers``,</span>
<span class="sd">                ``listvuln``, ``listwebclients``, ``listwebservers``,</span>
<span class="sd">                ``sumasset``, ``sumcce``, ``sumclassa``, ``sumclassb``,</span>
<span class="sd">                ``sumclassc``, ``sumcve``, ``sumdnsname``,</span>
<span class="sd">                ``sumfamily``, ``sumiavm``, ``sumid``, ``sumip``,</span>
<span class="sd">                ``summsbulletin``, ``sumprotocol``, ``sumremediation``,</span>
<span class="sd">                ``sumseverity``, ``sumuserresponsibility``, ``sumport``,</span>
<span class="sd">                ``trend``, ``vulndetails``, ``vulnipdetail``, ``vulnipsummary``</span>
<span class="sd">            view (str, optional):</span>
<span class="sd">                The type of vulnerability slice you&#39;d like to have returned.</span>
<span class="sd">                The returned data can be either ``all``, ``new``, or ``patched``.</span>
<span class="sd">                If no view is specified, then the default will be ``all``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`AnalysisResultsIterator`:</span>
<span class="sd">                An iterator object handling data pagination.</span>
<span class="sd">        Examples:</span>
<span class="sd">            A quick example showing how to get the information for a specific</span>
<span class="sd">            scan from SecurityCenter.  As the default is for the scan method to</span>
<span class="sd">            return data from the vulndetails tool, we can handle this without</span>
<span class="sd">            actually doing anything other than calling</span>
<span class="sd">            &gt;&gt;&gt; for vuln in sc.analysis.scan(1):</span>
<span class="sd">            ...     pprint(vuln)</span>
<span class="sd">            To ask for a specific subset of information (like only critical and</span>
<span class="sd">            exploitable vulns) you&#39;d want to pass the filter tuples into the</span>
<span class="sd">            query like so:</span>
<span class="sd">            &gt;&gt;&gt; vulns = sc.analysis.scan(1</span>
<span class="sd">            ...    (&#39;severity&#39;, &#39;=&#39;, &#39;4&#39;),</span>
<span class="sd">            ...    (&#39;exploitAvailable&#39;, &#39;=&#39;, &#39;true&#39;))</span>
<span class="sd">            To request a different data format (like maybe an IP summary of</span>
<span class="sd">            vulns) you just need to specify the appropriate tool:</span>
<span class="sd">            &gt;&gt;&gt; ips = sc.analysis.scan(1</span>
<span class="sd">            ...    (&#39;severity&#39;, &#39;=&#39;, &#39;4&#39;),</span>
<span class="sd">            ...    (&#39;exploitAvailable&#39;, &#39;=&#39;, &#39;true&#39;), tool=&#39;sumip&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_id&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;scan_id&#39;</span><span class="p">,</span> <span class="n">scan_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">vulns</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span></div>
<div class="viewcode-block" id="AnalysisAPI.events"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI.events">[docs]</a>    <span class="k">def</span> <span class="nf">events</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Queries the analysis API for event data from the Log Correlation Engine</span>
<span class="sd">        :sc-api:`analysis: event-type &lt;Analysis.html#AnalysisRESTReference-EventType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            filters (tuple, optional):</span>
<span class="sd">                The analysis module provides a more compact way to write filters</span>
<span class="sd">                to the analysis endpoint.  The purpose here is to aid in more</span>
<span class="sd">                readable code and reduce the amount of boilerplate that must be</span>
<span class="sd">                written to support a filtered call to analysis.  The format is</span>
<span class="sd">                simply a list of tuples.  Each tuple is broken down into</span>
<span class="sd">                (field, operator, value).</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                The number of pages to query.  Default is all.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many entries should be in each page?  Default is 200.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                How many entries to skip before processing.  Default is 0.</span>
<span class="sd">            source (str, optional):</span>
<span class="sd">                The data source location.  Allowed sources are ``lce``</span>
<span class="sd">                and ``archive``.  Defaults to ``lce``.</span>
<span class="sd">            silo_id (int, optional):</span>
<span class="sd">                If a silo id is specified, then the results fetched will be from</span>
<span class="sd">                the lce silo specified and not from the cumulative result set.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                The analysis tool for formatting and returning a specific view</span>
<span class="sd">                into the information.  If no tool is specified, the default will</span>
<span class="sd">                be ``vulndetails``.  Available tools are:</span>
<span class="sd">                ``listdata``, ``sumasset``, ``sumclassa``, ``sumclassb``,</span>
<span class="sd">                ``sumclassc``, ``sumconns``, ``sumdate``, ``sumdstip``,</span>
<span class="sd">                ``sumevent``, ``sumevent2``, ``sumip``, ``sumport``,</span>
<span class="sd">                ``sumprotocol``, ``sumsrcip``, ``sumtime``, ``sumtype``,</span>
<span class="sd">                ``sumuser``, ``syslog``, ``timedist``</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`AnalysisResultsIterator`:</span>
<span class="sd">                An iterator object handling data pagination.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;event&#39;</span><span class="p">,</span> <span class="s1">&#39;sourceType&#39;</span><span class="p">:</span> <span class="s1">&#39;lce&#39;</span><span class="p">}</span>
        <span class="k">if</span> <span class="s1">&#39;source&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;sourceType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;source&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;source&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;lce&#39;</span><span class="p">,</span> <span class="s1">&#39;archive&#39;</span><span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">)</span>
            <span class="k">if</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;source&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;archive&#39;</span><span class="p">:</span>
                <span class="k">if</span> <span class="s1">&#39;silo_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                    <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;view&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;silo_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;silo_id&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">else</span><span class="p">:</span>
                    <span class="k">raise</span> <span class="n">UnexpectedValueError</span><span class="p">(</span>
                        <span class="s1">&#39;silo_id is required for archive source&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;tool&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tool&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;listdata&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumasset&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassa&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassb&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumclassc&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumconns&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumdate&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumdstip&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumevent&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumevent2&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumip&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumport&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumprotocol&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumsrcip&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumtime&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumtype&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumuser&#39;</span><span class="p">,</span>
                <span class="s1">&#39;syslog&#39;</span><span class="p">,</span>
                <span class="s1">&#39;timedist&#39;</span><span class="p">,</span>
            <span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;syslog&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;payload&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">payload</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;event&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_analysis</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span></div>
    <span class="c1"># not sure what the user datatype is, however I haven&#39;t seen any use-cases</span>
    <span class="c1"># for this datatype.  leaving the method here, just commented out in-case</span>
    <span class="c1"># it needs some love and attention at a later date.</span>
    <span class="c1">#def user(self, *filters, **kw):</span>
    <span class="c1">#    &#39;&#39;&#39;</span>
    <span class="c1">#    &#39;&#39;&#39;</span>
    <span class="c1">#    payload = {&#39;type&#39;: &#39;user&#39;}</span>
    <span class="c1">#    kw[&#39;payload&#39;] = payload</span>
    <span class="c1">#    kw[&#39;tool&#39;] = &#39;user&#39;</span>
    <span class="c1">#    kw[&#39;type&#39;] = &#39;user&#39;</span>
    <span class="c1">#    return self._analysis(*filters, **kw)</span>
<div class="viewcode-block" id="AnalysisAPI.console"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI.console">[docs]</a>    <span class="k">def</span> <span class="nf">console</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Queries the analysis API for log data from the Tenable.sc Console itself.</span>
<span class="sd">        :sc-api:`analysis: sclog-type &lt;Analysis.html#AnalysisRESTReference-SCLogType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            filters (tuple, optional):</span>
<span class="sd">                The analysis module provides a more compact way to write filters</span>
<span class="sd">                to the analysis endpoint.  The purpose here is to aid in more</span>
<span class="sd">                readable code and reduce the amount of boilerplate that must be</span>
<span class="sd">                written to support a filtered call to analysis.  The format is</span>
<span class="sd">                simply a list of tuples.  Each tuple is broken down into</span>
<span class="sd">                (field, operator, value).</span>
<span class="sd">            date (str, optional):</span>
<span class="sd">                A date in YYYYMM format.  the default is simply &quot;all&quot;.</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                The number of pages to query.  Default is all.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many entries should be in each page?  Default is 200.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                How many entries to skip before processing.  Default is 0.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:` AnalysisResultsIterator`:</span>
<span class="sd">                An iterator object handling data pagination.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;payload&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;scLog&#39;</span><span class="p">,</span>
            <span class="s1">&#39;date&#39;</span><span class="p">:</span> <span class="s1">&#39;all&#39;</span> <span class="k">if</span> <span class="s1">&#39;date&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span> <span class="k">else</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;date&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;date&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="p">}</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;scLog&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;scLog&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_analysis</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span></div>
<div class="viewcode-block" id="AnalysisAPI.mobile"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.analysis.AnalysisAPI.mobile">[docs]</a>    <span class="k">def</span> <span class="nf">mobile</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Queries the analysis API for mobile data collected from querying one or</span>
<span class="sd">        many MDM solutions.</span>
<span class="sd">        :sc-api:`analysis: mobile-type &lt;Analysis.html#AnalysisRESTReference-MobileType&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            filters (tuple, optional):</span>
<span class="sd">                The analysis module provides a more compact way to write filters</span>
<span class="sd">                to the analysis endpoint.  The purpose here is to aid in more</span>
<span class="sd">                readable code and reduce the amount of boilerplate that must be</span>
<span class="sd">                written to support a filtered call to analysis.  The format is</span>
<span class="sd">                simply a list of tuples.  Each tuple is broken down into</span>
<span class="sd">                (field, operator, value).</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                The number of pages to query.  Default is all.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many entries should be in each page?  Default is 200.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                How many entries to skip before processing.  Default is 0.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                The analysis tool for formatting and returning a specific view</span>
<span class="sd">                into the information.  If no tool is specified, the default will</span>
<span class="sd">                be ``vulndetails``.  Available tools are:</span>
<span class="sd">                ``listvuln``, ``sumdeviceid``, ``summdmuser``, ``summodel``,</span>
<span class="sd">                ``sumoscpe``, ``sumpluginid``, ``sumseverity``, ``vulndetails``</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`AnalysisResultsIterator`:</span>
<span class="sd">                An iterator object handling data pagination.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;mobile&#39;</span><span class="p">,</span> <span class="s1">&#39;sourceType&#39;</span><span class="p">:</span> <span class="s1">&#39;cumulative&#39;</span><span class="p">}</span>
        <span class="k">if</span> <span class="s1">&#39;tool&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tool&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;listvuln&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumdeviceid&#39;</span><span class="p">,</span>
                <span class="s1">&#39;summdmuser&#39;</span><span class="p">,</span>
                <span class="s1">&#39;summodel&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumoscpe&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumpluginid&#39;</span><span class="p">,</span>
                <span class="s1">&#39;sumseverity&#39;</span><span class="p">,</span>
                <span class="s1">&#39;vulndetails&#39;</span>
            <span class="p">],</span>  <span class="n">case</span><span class="o">=</span><span class="s1">&#39;lower&#39;</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;vulndetails&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;payload&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">payload</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;mobile&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_analysis</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.analysis</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
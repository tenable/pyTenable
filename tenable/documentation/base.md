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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.base</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.base</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Common Themes</span>
<span class="sd">=============</span>
<span class="sd">Tenable.sc CRUD within pyTenable</span>
<span class="sd">--------------------------------</span>
<span class="sd">pyTenable allows for the ability to leverage both the naturalized inputs as well</span>
<span class="sd">as passing the raw parameters within the same structure.  In some cases this</span>
<span class="sd">doesn&#39;t seem immediately obvious, however allows for the ability to pass</span>
<span class="sd">parameters that either haven&#39;t yet been, or in some cases, may never be</span>
<span class="sd">interpreted by the library.</span>
<span class="sd">For example, in the alerts API, you could pass the snake_cased</span>
<span class="sd">``always_exec_on_trigger`` or you could pass what the API endpoint itself</span>
<span class="sd">expects, which is ``executeOnEveryTrigger``.  The snake-cased version expects a</span>
<span class="sd">boolean value, which will be converted into the string value that camelCased</span>
<span class="sd">variant expects.  You&#39;ll see this behavior a lot throughout the library, and is</span>
<span class="sd">intended to allow you to sidestep most things should you need to.  For example,</span>
<span class="sd">in the alerts API again, you may not want to pass a trigger as</span>
<span class="sd">``trigger=(&#39;sumip&#39;, &#39;&gt;=&#39;, &#39;100&#39;)`` and instead pass as the parameters that are</span>
<span class="sd">to be written into the JSON request:</span>
<span class="sd">``triggerName=&#39;sumip&#39;, triggerOperator=&#39;&gt;=&#39;, triggerValue=&#39;100&#39;``.  Both of</span>
<span class="sd">these methods will produce the same JSON request, and the the option is yours</span>
<span class="sd">to use the right way for the job.</span>
<span class="sd">Along these same lines, its possible to see how the JSON documents are being</span>
<span class="sd">constructed by simply looking at the ``_constructor`` methods for each</span>
<span class="sd">APIEndpoint class.  If pyTenable is getting in your way, you can almost always</span>
<span class="sd">sidestep it and pass the exact dictionary you wish to pass on to the API.</span>
<span class="sd">Schedule Dictionaries</span>
<span class="sd">---------------------</span>
<span class="sd">A dictionary detailing the repeating schedule within Tenable.sc.  This</span>
<span class="sd">dictionary consists of 1 or 3 parameters, depending on the type of schedule.</span>
<span class="sd">In all of the definitions except ``ical``, a  single parameter of ``type`` is</span>
<span class="sd">passed with lone of the following values: ``ical``, ``never``, ``rollover``, and</span>
<span class="sd">``template``.  If no document is specified, then the default of ``never`` is</span>
<span class="sd">assumed.  For repeating scans, you&#39;ll have to use the type of ``ical`` and also</span>
<span class="sd">specify the ``start`` and ``repeatRule`` parameters as well.  The ``start``</span>
<span class="sd">parameter is an</span>
<span class="sd">`iCal DateTime Form #3 &lt;https://tools.ietf.org/html/rfc5545#section-3.3.5&gt;`_</span>
<span class="sd">formatted string specifying the date and time in which to start the repeating</span>
<span class="sd">event.  The ``repeatRule`` parameter is an</span>
<span class="sd">`iCal Recurrence Rule &lt;https://tools.ietf.org/html/rfc5545#section-3.3.10&gt;`_</span>
<span class="sd">formatted string.</span>
<span class="sd">* Example Never Declaration:</span>
<span class="sd">.. code-block:: python</span>
<span class="sd">    {&#39;type&#39;: &#39;never&#39;}</span>
<span class="sd">* Example daily event starting at 9am Eastern</span>
<span class="sd">.. code-block:: python</span>
<span class="sd">    {</span>
<span class="sd">        &#39;type&#39;: &#39;ical&#39;,</span>
<span class="sd">        &#39;start&#39;: &#39;TZID=America/New_York:20190214T090000&#39;,</span>
<span class="sd">        &#39;repeatRule&#39;: &#39;FREQ=DAILY;INTERVAL=1&#39;</span>
<span class="sd">    }</span>
<span class="sd">* Example weekly event every Saturday at 8:30pm Eastern</span>
<span class="sd">.. code-block:: python</span>
<span class="sd">    {</span>
<span class="sd">        &#39;type&#39;: &#39;ical&#39;,</span>
<span class="sd">        &#39;start&#39;: &#39;TZID=America/New_York:20190214T203000&#39;,</span>
<span class="sd">        &#39;repeatRule&#39;: &#39;FREQ=WEEKLY;BYDAY=SA;INTERVAL=1&#39;</span>
<span class="sd">    }</span>
<span class="sd">There are detailed instructions in the RFC documentation on how to construct</span>
<span class="sd">these recurrence rules.  Further there are some packages out there to aid in</span>
<span class="sd">converting more human-readable text into recurrence rules, such as the</span>
<span class="sd">`recurrent package &lt;https://pypi.org/project/recurrent/&gt;`_ for example.</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.base.v1</span> <span class="kn">import</span> <span class="n">APIResultsIterator</span>
<div class="viewcode-block" id="SCEndpoint"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.base.SCEndpoint">[docs]</a><span class="k">class</span> <span class="nc">SCEndpoint</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_combo_expansion</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">item</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Expands the asset combination expressions from nested tuples to the</span>
<span class="sd">        nested dictionary structure that&#39;s expected.</span>
<span class="sd">        Args:</span>
<span class="sd">            item</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The dictionary structure of the expanded asset list combinations.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># the operator conversion dictionary.  The UI uses &quot;and&quot;, &quot;or&quot;, and</span>
        <span class="c1"># &quot;not&quot; whereas the API uses &quot;intersection&quot;, &quot;union&quot;, and &quot;compliment&quot;.</span>
        <span class="c1"># if the user is passing us the tuples, lets assume that they are using</span>
        <span class="c1"># the UI definitions and not the API ones.</span>
        <span class="n">oper</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;and&#39;</span><span class="p">:</span> <span class="s1">&#39;intersection&#39;</span><span class="p">,</span>
            <span class="s1">&#39;or&#39;</span><span class="p">:</span> <span class="s1">&#39;union&#39;</span><span class="p">,</span>
            <span class="s1">&#39;not&#39;</span><span class="p">:</span> <span class="s1">&#39;complement&#39;</span>
        <span class="p">}</span>
        <span class="c1"># some simple checking to ensure that we are being passed good data</span>
        <span class="c1"># before we expand the tuple.</span>
        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">item</span><span class="p">)</span> <span class="o">&lt;</span> <span class="mi">2</span> <span class="ow">or</span> <span class="nb">len</span><span class="p">(</span><span class="n">item</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">3</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s1">&#39;</span><span class="si">{}</span><span class="s1"> must be exactly 1 operator and 1-2 items&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">item</span><span class="p">))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;operator&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="n">oper</span><span class="o">.</span><span class="n">keys</span><span class="p">())</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;operand1&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="nb">tuple</span><span class="p">))</span>
        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">item</span><span class="p">)</span> <span class="o">==</span> <span class="mi">3</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;operand2&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="nb">tuple</span><span class="p">))</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="n">oper</span><span class="p">[</span><span class="n">item</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">lower</span><span class="p">()]}</span>
        <span class="c1"># we need to expand the operand.  If the item is a nested tuple, then</span>
        <span class="c1"># we will call ourselves and pass the tuple.  If not, then we will</span>
        <span class="c1"># simply return a dictionary with the id value set to the integer that</span>
        <span class="c1"># was passed.</span>
        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">):</span>
            <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;operand1&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_combo_expansion</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">1</span><span class="p">])</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;operand1&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">1</span><span class="p">])}</span>
        <span class="c1"># if there are 2 operators in the tuple, then we will want to expand the</span>
        <span class="c1"># second one as well. If the item is a nested tuple, then we will call</span>
        <span class="c1"># ourselves and pass the tuple.  If not, then we will simply return a</span>
        <span class="c1"># dictionary with the id value set to the integer that was passed.</span>
        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">item</span><span class="p">)</span> <span class="o">==</span> <span class="mi">3</span><span class="p">:</span>
            <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">):</span>
                <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;operand2&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_combo_expansion</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">2</span><span class="p">])</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;operand2&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="n">item</span><span class="p">[</span><span class="mi">2</span><span class="p">])}</span>
        <span class="c1"># return the response to the caller.</span>
        <span class="k">return</span> <span class="n">resp</span>
    <span class="k">def</span> <span class="nf">_query_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Constructs an analysis query.  This part has been pulled out of the</span>
<span class="sd">        _analysis method and placed here so that it can be re-used in other</span>
<span class="sd">        part of the library.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;filters&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if filters are explicitly called, then we will replace the</span>
            <span class="c1"># implicit filters with the explicit ones and remove the entry from</span>
            <span class="c1"># the keywords dictionary</span>
            <span class="n">filters</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filters&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filters&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filters&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;query&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="s1">&#39;tool&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
                <span class="s1">&#39;tool&#39;</span><span class="p">:</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">],</span>
                <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span>
                <span class="s1">&#39;filters&#39;</span><span class="p">:</span> <span class="nb">list</span><span class="p">()</span>
            <span class="p">}</span>
            <span class="k">if</span> <span class="s1">&#39;query_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="c1"># Request the specific query ID provided and fetch only the filters</span>
                <span class="n">query_response</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span>
                    <span class="s1">&#39;query/</span><span class="si">{}</span><span class="s1">?fields=filters&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
                        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query_id&#39;</span><span class="p">]))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
                <span class="c1"># Extract the filters or set to null if nothing is returned</span>
                <span class="n">query_filters</span> <span class="o">=</span> <span class="n">query_response</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;filters&#39;</span><span class="p">,</span> <span class="nb">list</span><span class="p">())</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;filters&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">query_filters</span>
            <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">filters</span><span class="p">:</span>
                <span class="k">if</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;ticket&#39;</span><span class="p">:</span>
                    <span class="n">item</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;filterName&#39;</span><span class="p">:</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="n">f</span><span class="p">[</span><span class="mi">1</span><span class="p">]}</span>
                <span class="k">else</span><span class="p">:</span>
                    <span class="n">item</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;filterName&#39;</span><span class="p">:</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="n">f</span><span class="p">[</span><span class="mi">1</span><span class="p">]}</span>
                <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">f</span><span class="p">)</span> <span class="o">&gt;=</span> <span class="mi">3</span><span class="p">:</span>
                    <span class="k">if</span> <span class="p">(</span><span class="nb">isinstance</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">)</span>
                      <span class="ow">and</span> <span class="n">f</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;~&#39;</span> <span class="ow">and</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;asset&#39;</span><span class="p">):</span>
                        <span class="c1"># if this is a asset combination, then we will want to</span>
                        <span class="c1"># expand the tuple into the expected dictionary</span>
                        <span class="c1"># structure that the API is expecting.</span>
                        <span class="n">item</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_combo_expansion</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">])</span>
                    <span class="k">elif</span> <span class="p">(</span><span class="nb">isinstance</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">list</span><span class="p">)</span>
                      <span class="ow">and</span> <span class="nb">all</span><span class="p">(</span><span class="nb">isinstance</span><span class="p">(</span><span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">])):</span>
                        <span class="c1"># if the value is a list and all of the items within</span>
                        <span class="c1"># that list are integers, then we can safely assume that</span>
                        <span class="c1"># this is a list of integer ids that need to be expanded</span>
                        <span class="c1"># into a list of dictionaries.</span>
                        <span class="n">item</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[</span><span class="nb">dict</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="nb">str</span><span class="p">(</span><span class="n">i</span><span class="p">))</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">]]</span>
                    <span class="k">elif</span> <span class="p">(</span><span class="nb">isinstance</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span> <span class="ow">and</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;asset&#39;</span><span class="p">,]):</span>
                        <span class="c1"># If the value is an integer, then we will want to</span>
                        <span class="c1"># expand the value into a dictionary with an id attr.</span>
                        <span class="n">item</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">(</span><span class="nb">id</span><span class="o">=</span><span class="nb">str</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">]))</span>
                    <span class="k">else</span><span class="p">:</span>
                        <span class="c1"># if we don&#39;t have any specific conditions set, then</span>
                        <span class="c1"># simply return the value parameter assigned to the</span>
                        <span class="c1"># &quot;value&quot; attribute</span>
                        <span class="n">item</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span>
                <span class="c1"># Added this here to make the filter list overloadable.  As SC</span>
                <span class="c1"># only supports one filter of a given type, if an existing</span>
                <span class="c1"># filter is already in the list, we will overload it with the</span>
                <span class="c1"># new one.  This allows for the ability to overload query</span>
                <span class="c1"># filters if need be, or to overload a saved filterset that</span>
                <span class="c1"># someone is appending to.</span>
                <span class="n">flist</span> <span class="o">=</span> <span class="p">[</span><span class="n">i</span><span class="p">[</span><span class="s1">&#39;filterName&#39;</span><span class="p">]</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;filters&#39;</span><span class="p">]]</span>
                <span class="k">if</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">in</span> <span class="n">flist</span><span class="p">:</span>
                    <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;filters&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">pop</span><span class="p">(</span><span class="n">flist</span><span class="o">.</span><span class="n">index</span><span class="p">(</span><span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">]))</span>
                <span class="c1"># Add the newly expanded filter to the filters list as long as</span>
                <span class="c1"># both the operator and value are not None.  If both are none,</span>
                <span class="c1"># then skip appending.  This should allow for effectively</span>
                <span class="c1"># removing an unwanted filter from a query if a query id is</span>
                <span class="c1"># specified.</span>
                <span class="k">if</span> <span class="n">f</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">!=</span> <span class="kc">None</span> <span class="ow">and</span> <span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span> <span class="o">!=</span> <span class="kc">None</span><span class="p">:</span>
                    <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;filters&#39;</span><span class="p">]</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">item</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
    <span class="k">def</span> <span class="nf">_schedule_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">item</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles creation of the schedule sub-document.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;schedule:item&#39;</span><span class="p">,</span> <span class="n">item</span><span class="p">,</span> <span class="nb">dict</span><span class="p">)</span>
        <span class="n">item</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;schedule:type&#39;</span><span class="p">,</span>  <span class="n">item</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">),</span> <span class="nb">str</span><span class="p">,</span>
            <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ical&#39;</span><span class="p">,</span> <span class="s1">&#39;dependent&#39;</span><span class="p">,</span> <span class="s1">&#39;never&#39;</span><span class="p">,</span> <span class="s1">&#39;rollover&#39;</span><span class="p">,</span> <span class="s1">&#39;template&#39;</span><span class="p">,</span> <span class="s1">&#39;now&#39;</span><span class="p">],</span>
            <span class="n">default</span><span class="o">=</span><span class="s1">&#39;never&#39;</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;ical&#39;</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;schedule:start&#39;</span><span class="p">,</span> <span class="n">item</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;start&#39;</span><span class="p">),</span> <span class="nb">str</span><span class="p">)</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;schedule:repeatRule&#39;</span><span class="p">,</span> <span class="n">item</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;repeatRule&#39;</span><span class="p">),</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">item</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;dependent&#39;</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;schedule:dependentID&#39;</span><span class="p">,</span> <span class="n">item</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;dependentID&#39;</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">return</span> <span class="n">item</span></div>
<div class="viewcode-block" id="SCResultsIterator"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.base.SCResultsIterator">[docs]</a><span class="k">class</span> <span class="nc">SCResultsIterator</span><span class="p">(</span><span class="n">APIResultsIterator</span><span class="p">):</span>
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
        <span class="n">query</span><span class="p">[</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span>
        <span class="n">query</span><span class="p">[</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span>
        <span class="c1"># Lets actually call the API for the data at this point.</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_resource</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">query</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()</span>
        <span class="c1"># Now that we have the response, lets reset any counters we need to,</span>
        <span class="c1"># and increment things like the page counter, offset, etc.</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">page_count</span> <span class="o">=</span> <span class="mi">0</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_pages_requested</span> <span class="o">+=</span> <span class="mi">1</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_offset</span> <span class="o">+=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_raw</span> <span class="o">=</span> <span class="n">resp</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">page</span> <span class="o">=</span> <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="c1"># As no total is returned via the API, we will simply need to re-compute</span>
        <span class="c1"># the total to be N+1 every page as long as the page of data is equal to</span>
        <span class="c1"># the limit.  If we ever get a page of data that is less than the limit,</span>
        <span class="c1"># then we will set the total to be the count + page length.</span>
        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">])</span> <span class="o">&lt;</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">total</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">count</span> <span class="o">+</span> <span class="nb">len</span><span class="p">(</span><span class="n">resp</span><span class="p">[</span><span class="s1">&#39;response&#39;</span><span class="p">])</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">total</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">count</span> <span class="o">+</span> <span class="bp">self</span><span class="o">.</span><span class="n">_limit</span> <span class="o">+</span> <span class="mi">1</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.base</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
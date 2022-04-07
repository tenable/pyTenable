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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.alerts</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.alerts</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Alerts</span>
<span class="sd">======</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">`Alert &lt;https://docs.tenable.com/sccv/api/Alert.html&gt;`_ API.</span>
<span class="sd">Methods available on ``sc.alerts``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AlertAPI</span>
<span class="sd">    :members:</span>
<span class="sd">.. _iCal Date-Time:</span>
<span class="sd">    https://tools.ietf.org/html/rfc5545#section-3.3.5</span>
<span class="sd">.. _iCal Recurrence Rule:</span>
<span class="sd">    https://tools.ietf.org/html/rfc5545#section-3.3.10</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<div class="viewcode-block" id="AlertAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI">[docs]</a><span class="k">class</span> <span class="nc">AlertAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles building an alert document.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># call the analysis query constructor to assemble a query.</span>
        <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">filters</span><span class="p">)</span> <span class="o">&gt;</span> <span class="mi">0</span><span class="p">:</span>
            <span class="c1"># checking to see if data_type was passed.  If it wasn&#39;t then we</span>
            <span class="c1"># will set the value to the default of &#39;vuln&#39;.</span>
            <span class="k">if</span> <span class="s1">&#39;data_type&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;vuln&#39;</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_type&#39;</span><span class="p">]</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;&#39;</span>
            <span class="n">kw</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_type&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">][</span><span class="s1">&#39;tool&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">])</span>
        <span class="k">elif</span> <span class="s1">&#39;query_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;query&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;query&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;query&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;always_exec_on_trigger&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># executeOnEveryTrigger expected a boolean response as a lower-case</span>
            <span class="c1"># string.  We will accept a boolean and then transform it into a</span>
            <span class="c1"># string value.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;executeOnEveryTrigger&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;always_exec_on_trigger&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;always_exec_on_trigger&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;always_exec_on_trigger&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;trigger&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># here we will be expanding the trigger from the common format of</span>
            <span class="c1"># tuples that we are using within pytenable into the native</span>
            <span class="c1"># supported format that SecurityCenter expects.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;trigger&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;trigger&#39;</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;triggerName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;triggerName&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;trigger&#39;</span><span class="p">][</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;triggerOperator&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;triggerOperator&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;trigger&#39;</span><span class="p">][</span><span class="mi">1</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;&gt;=&#39;</span><span class="p">,</span> <span class="s1">&#39;&lt;=&#39;</span><span class="p">,</span> <span class="s1">&#39;=&#39;</span><span class="p">,</span> <span class="s1">&#39;!=&#39;</span><span class="p">])</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;triggerValue&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;triggerValue&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;trigger&#39;</span><span class="p">][</span><span class="mi">2</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;trigger&#39;</span><span class="p">])</span>
        <span class="c1"># hand off the building the schedule sub-document to the schedule</span>
        <span class="c1"># document builder.</span>
        <span class="k">if</span> <span class="s1">&#39;schedule&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;schedule&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schedule_constructor</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;schedule&#39;</span><span class="p">])</span>
        <span class="c1"># FR: at some point we should start looking into checking and</span>
        <span class="c1">#     normalizing the action document.</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="AlertAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of alerts.</span>
<span class="sd">        :sc-api:`alert: list &lt;Alert.html#AlertRESTReference-/alert&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each alert.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                A list of alert resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for alert in sc.alerts.list()[&#39;manageable&#39;]:</span>
<span class="sd">            ...     pprint(alert)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;alert&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AlertAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific alert.</span>
<span class="sd">        :sc-api:`alert: details &lt;Alert.html#AlertRESTReference-/alert/{id}&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the alert.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The alert resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; alert = sc.alerts.detail(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(alert)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;alert/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AlertAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new alert.  The fields below are explicitly checked, however</span>
<span class="sd">        any additional parameters mentioned in the API docs can be passed to the</span>
<span class="sd">        document constructor.</span>
<span class="sd">        :sc-api:&#39;alert: create &lt;Alert.html#alert_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            *filters (tuple):</span>
<span class="sd">                A filter expression.  Refer to the detailed description within</span>
<span class="sd">                the analysis endpoint documentation for more details on how to</span>
<span class="sd">                formulate filter expressions.</span>
<span class="sd">            data_type (str):</span>
<span class="sd">                The type of filters being used.  Must be of type ``lce``,</span>
<span class="sd">                ``ticket``, ``user``, or ``vuln``.  If no data-type is</span>
<span class="sd">                specified, then the default of ``vuln`` will be set.</span>
<span class="sd">            name (str): The name of the alert.</span>
<span class="sd">            description (str, optional): A description for the alert.</span>
<span class="sd">            trigger (tuple):</span>
<span class="sd">                A tuple in the filter-tuple format detailing what would</span>
<span class="sd">                constitute a trigger.  For example: ``(&#39;sumip&#39;, &#39;=&#39;, &#39;1000&#39;)``.</span>
<span class="sd">            always_exec_on_trigger (bool, optional):</span>
<span class="sd">                Should the trigger always execute when the trigger fires, or</span>
<span class="sd">                only execute when the returned data changes?</span>
<span class="sd">                Default is ``False``.</span>
<span class="sd">            schedule (dict, optional):</span>
<span class="sd">                This is the schedule dictionary that will inform Tenable.sc how</span>
<span class="sd">                often to run the alert.  If left unspecified then we will</span>
<span class="sd">                default to ``{&#39;type&#39;: &#39;never&#39;}``.</span>
<span class="sd">            action (list):</span>
<span class="sd">                The action(s) that will be performed when the alert trigger</span>
<span class="sd">                fires.  Each action is a dictionary detailing what type of</span>
<span class="sd">                action to take, and the details surrounding that action.  The</span>
<span class="sd">                supported type of actions are ``email``, ``notifications``,</span>
<span class="sd">                ``report``, ``scan``, ``syslog``, and ``ticket``.  The following</span>
<span class="sd">                examples lay out each type of action as an example:</span>
<span class="sd">                * Email action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;email&#39;,</span>
<span class="sd">                     &#39;subject&#39;: &#39;Example Email Subject&#39;,</span>
<span class="sd">                     &#39;message&#39;: &#39;Example Email Body&#39;</span>
<span class="sd">                     &#39;addresses&#39;: &#39;user1@company.com\\nuser2@company.com&#39;,</span>
<span class="sd">                     &#39;users&#39;: [{&#39;id&#39;: 1}, {&#39;id&#39;: 2}],</span>
<span class="sd">                     &#39;includeResults&#39;: &#39;true&#39;}</span>
<span class="sd">                * Notification action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;notification&#39;,</span>
<span class="sd">                     &#39;message&#39;: &#39;Example notification&#39;,</span>
<span class="sd">                     &#39;users&#39;: [{&#39;id&#39;: 1}, {&#39;id&#39;: 2}]}</span>
<span class="sd">                * Report action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;report&#39;,</span>
<span class="sd">                     &#39;report&#39;: {&#39;id&#39;: 1}}</span>
<span class="sd">                * Scan action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;scan&#39;,</span>
<span class="sd">                     &#39;scan&#39;: {&#39;id&#39;: 1}}</span>
<span class="sd">                * Syslog action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;syslog&#39;,</span>
<span class="sd">                     &#39;host&#39;: &#39;127.0.0.1&#39;,</span>
<span class="sd">                     &#39;port&#39;: &#39;514&#39;,</span>
<span class="sd">                     &#39;message&#39;: &#39;Example Syslog Message&#39;,</span>
<span class="sd">                     &#39;severity&#39;: &#39;Critical&#39;}</span>
<span class="sd">                * Ticket action type:</span>
<span class="sd">                .. code-block:: python</span>
<span class="sd">                    {&#39;type&#39;: &#39;ticket&#39;,</span>
<span class="sd">                     &#39;assignee&#39;: {&#39;id&#39;: 1},</span>
<span class="sd">                     &#39;name&#39;: &#39;Example Ticket Name&#39;,</span>
<span class="sd">                     &#39;description&#39;: &#39;Example Ticket Description&#39;,</span>
<span class="sd">                     &#39;notes&#39;: &#39;Example Ticket Notes&#39;}</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The alert resource created.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.alerts.create(</span>
<span class="sd">            ...     (&#39;severity&#39;, &#39;=&#39;, &#39;3,4&#39;),</span>
<span class="sd">            ...     (&#39;exploitAvailable&#39;, &#39;=&#39;, &#39;true&#39;),</span>
<span class="sd">            ...     trigger=(&#39;sumip&#39;, &#39;&gt;=&#39;, &#39;100&#39;),</span>
<span class="sd">            ...     name=&#39;Too many High or Critical and Exploitable&#39;,</span>
<span class="sd">            ...     action=[{</span>
<span class="sd">            ...         &#39;type&#39;: &#39;notification&#39;,</span>
<span class="sd">            ...         &#39;message&#39;: &#39;Too many High or Crit Exploitable Vulns&#39;,</span>
<span class="sd">            ...         &#39;users&#39;: [{&#39;id&#39;: 1}]</span>
<span class="sd">            ...     }])</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;alert&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AlertAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates an existing alert.  All fields are optional and will overwrite</span>
<span class="sd">        the existing value.</span>
<span class="sd">        :sc-api:`alert: update &lt;Alert.html#alert_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            if (int): The alert identifier.</span>
<span class="sd">            *filters (tuple):</span>
<span class="sd">                A filter expression.  Refer to the detailed description within</span>
<span class="sd">                the analysis endpoint documentation for more details on how to</span>
<span class="sd">                formulate filter expressions.</span>
<span class="sd">            data_type (str):</span>
<span class="sd">                The type of filters being used.  Must be of type ``lce``,</span>
<span class="sd">                ``ticket``, ``user``, or ``vuln``.  If no data-type is</span>
<span class="sd">                specified, then the default of ``vuln`` will be set.</span>
<span class="sd">            name (str, optional): The name of the alert.</span>
<span class="sd">            description (str, optional): A description for the alert.</span>
<span class="sd">            trigger (tuple, optional):</span>
<span class="sd">                A tuple in the filter-tuple format detailing what would</span>
<span class="sd">                constitute a trigger.  For example: ``(&#39;sumip&#39;, &#39;=&#39;, &#39;1000&#39;)``.</span>
<span class="sd">            always_exec_on_trigger (bool, optional):</span>
<span class="sd">                Should the trigger always execute when the trigger fires, or</span>
<span class="sd">                only execute when the returned data changes?</span>
<span class="sd">                Default is ``False``.</span>
<span class="sd">            schedule (dict, optional):</span>
<span class="sd">                This is the schedule dictionary that will inform Tenable.sc how</span>
<span class="sd">                often to run the alert.  If left unspecified then we will</span>
<span class="sd">                default to ``{&#39;type&#39;: &#39;never&#39;}``.</span>
<span class="sd">            action (list):</span>
<span class="sd">                The action(s) that will be performed when the alert trigger</span>
<span class="sd">                fires.  Each action is a dictionary detailing what type of</span>
<span class="sd">                action to take, and the details surrounding that action.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The modified alert resource.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.alerts.update(1, name=&#39;New Alert Name&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;alert/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AlertAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Deletes the specified alert.</span>
<span class="sd">        :sc-api:`alert: delete &lt;Alert.html#alert_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The alert identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                The response code of the action.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.alerts.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;alert/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AlertAPI.execute"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.alerts.AlertAPI.execute">[docs]</a>    <span class="k">def</span> <span class="nf">execute</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Executes the specified alert.</span>
<span class="sd">        :sc-api:`alert: execute &lt;Alert.html#AlertRESTReference-/alert/{id}/execute&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The alert identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The alert resource.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;alert/</span><span class="si">{}</span><span class="s1">/execute&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.alerts</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
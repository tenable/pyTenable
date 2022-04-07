
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.plugins &#8212; pyTenable  documentation</title>
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
          <li class="nav-item nav-item-1"><a href="../../index.md" >Module code</a> &#187;</li>
          <li class="nav-item nav-item-2"><a href="../sc.md" accesskey="U">tenable.sc</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.sc.plugins</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.plugins</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Plugins</span>
<span class="sd">=======</span>

<span class="sd">The following methods allow for interaction with the Tenable.sc</span>
<span class="sd">:sc-api:`Plugins &lt;Plugin.html&gt;` API.  These items are typically seen under the</span>
<span class="sd">**Plugins** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.plugins``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: PluginAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span><span class="p">,</span> <span class="n">SCResultsIterator</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">UnexpectedValueError</span>


<div class="viewcode-block" id="PluginResultsIterator"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginResultsIterator">[docs]</a><span class="k">class</span> <span class="nc">PluginResultsIterator</span><span class="p">(</span><span class="n">SCResultsIterator</span><span class="p">):</span>
    <span class="k">pass</span></div>


<div class="viewcode-block" id="PluginAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI">[docs]</a><span class="k">class</span> <span class="nc">PluginAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Constructs the plugin query.</span>
<span class="sd">        &#39;&#39;&#39;</span>

        <span class="k">if</span> <span class="s1">&#39;fields&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                     <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fields&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)])</span>

        <span class="k">if</span> <span class="s1">&#39;filter&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># break down the filter tuple into the various query parameters</span>
            <span class="c1"># that the plugin api expects.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">)</span>
            <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">])</span> <span class="o">!=</span> <span class="mi">3</span><span class="p">:</span>
                <span class="k">raise</span> <span class="n">UnexpectedValueError</span><span class="p">(</span>
                    <span class="s1">&#39;the filter tuple must be name, operator, value.&#39;</span><span class="p">)</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filterField&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:field&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">][</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;op&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:operator&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">][</span><span class="mi">1</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                                   <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;eq&#39;</span><span class="p">,</span> <span class="s1">&#39;gt&#39;</span><span class="p">,</span> <span class="s1">&#39;gte&#39;</span><span class="p">,</span> <span class="s1">&#39;like&#39;</span><span class="p">,</span> <span class="s1">&#39;lt&#39;</span><span class="p">,</span> <span class="s1">&#39;lte&#39;</span><span class="p">])</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:value&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">][</span><span class="mi">2</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;filter&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;sort_field&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the snake_cased variant of the parameter to the camelCased</span>
            <span class="c1"># variant that the API expects to see.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sortField&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_field&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;sort_direction&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># convert the snake_cased variant of the parameter to the camelCased</span>
            <span class="c1"># variant that the API expects to see.</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sortDirection&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_direction&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sort_direction&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ASC&#39;</span><span class="p">,</span> <span class="s1">&#39;DESC&#39;</span><span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;sort_direction&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;since&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># The since parameter should be an integer.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;since&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;since&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="c1"># Validate that the plugin type is what&#39;s expected.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;active&#39;</span><span class="p">,</span> <span class="s1">&#39;all&#39;</span><span class="p">,</span> <span class="s1">&#39;compliance&#39;</span><span class="p">,</span> <span class="s1">&#39;custom&#39;</span><span class="p">,</span>
                <span class="s1">&#39;lce&#39;</span><span class="p">,</span> <span class="s1">&#39;notPassive&#39;</span><span class="p">,</span> <span class="s1">&#39;passive&#39;</span>
            <span class="p">],</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;all&#39;</span><span class="p">)</span>

        <span class="c1"># While the iterator will handle the offset &amp; limits, a raw json result</span>
        <span class="c1"># may be requested instead.</span>
        <span class="k">if</span> <span class="s1">&#39;offset&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;offset&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;offset&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;limit&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;limit&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span> <span class="o">+</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;startOffset&#39;</span><span class="p">,</span> <span class="mi">0</span><span class="p">)</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;limit&#39;</span><span class="p">]</span>

        <span class="c1"># Pages and json_result parameters should be removed from the document</span>
        <span class="c1"># if they exist.</span>
        <span class="k">if</span> <span class="s1">&#39;pages&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;pages&#39;</span><span class="p">]</span>

        <span class="k">if</span> <span class="s1">&#39;json_result&#39;</span> <span class="ow">in</span> <span class="n">kwargs</span><span class="p">:</span>
            <span class="k">del</span> <span class="n">kwargs</span><span class="p">[</span><span class="s1">&#39;json_result&#39;</span><span class="p">]</span>

        <span class="c1"># Return the modified keyword dict to the caller.</span>
        <span class="k">return</span> <span class="n">kwargs</span>

<div class="viewcode-block" id="PluginAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of plugins.</span>

<span class="sd">        :sc-api:`plugins: list &lt;Plugin.html#PluginRESTReference-/plugin&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">            filter (tuple, optional):</span>
<span class="sd">                A filter tuple for which to filter the plugins.  Filter tuples</span>
<span class="sd">                must be ``(&#39;name&#39;, &#39;operator&#39;, &#39;value&#39;)`` and follow a similar</span>
<span class="sd">                yet different format to the analysis filters.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many records should be returned in each page of data.  If</span>
<span class="sd">                none is specified, the default is 1000 records.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                At what offset within the data should we start returning data.</span>
<span class="sd">                If none is specified, the default is 0.</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                How many pages of data should we return.  If none is specified</span>
<span class="sd">                then all pages will return.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of plugins to return.  Available types are ``active``,</span>
<span class="sd">                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and</span>
<span class="sd">                ``passive``.  If nothing is specified, then ``all`` is assumed.</span>

<span class="sd">        Returns:</span>
<span class="sd">            PluginResultsIterator: an iterator object handling data pagination.</span>

<span class="sd">        Examples:</span>
<span class="sd">            To retrieve all of the plugins, you&#39;ll simply need to call the list</span>
<span class="sd">            method like so:</span>

<span class="sd">            &gt;&gt;&gt; plugins = sc.plugins.list()</span>
<span class="sd">            &gt;&gt;&gt; for plugin in plugins:</span>
<span class="sd">            ...     pprint(plugin)</span>

<span class="sd">            If you only want the plugins with java in the name, you&#39;d run a</span>
<span class="sd">            query similar to this one:</span>

<span class="sd">            &gt;&gt;&gt; plugins = sc.plugins.list(</span>
<span class="sd">            ...     filter=(&#39;name&#39;, &#39;like&#39;, &#39;java&#39;))</span>

<span class="sd">            For just the active plugins, we&#39;d run:</span>

<span class="sd">            &gt;&gt;&gt; plugins = sc.plugins.list(type=&#39;active&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">offset</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="mi">0</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">limit</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="mi">1000</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">pages</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">json_result</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;json_result&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

        <span class="k">if</span> <span class="n">json_result</span><span class="p">:</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">query</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="k">return</span> <span class="n">PluginResultsIterator</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="p">,</span>
                                         <span class="n">_resource</span><span class="o">=</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span>
                                         <span class="n">_offset</span><span class="o">=</span><span class="n">offset</span><span class="p">,</span>
                                         <span class="n">_limit</span><span class="o">=</span><span class="n">limit</span><span class="p">,</span>
                                         <span class="n">_query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
                                         <span class="n">_pages_total</span><span class="o">=</span><span class="n">pages</span><span class="p">)</span></div>

<div class="viewcode-block" id="PluginAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific plugin.</span>

<span class="sd">        :sc-api:`plugins: details &lt;Plugin.html#PluginRESTReference-/plugin/{id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            plugin_id (int): The identifier for the plugin.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The plugin resource record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; plugin = sc.plugins.detail(19506)</span>
<span class="sd">            &gt;&gt;&gt; pprint(plugin)</span>
<span class="sd">       &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;plugin/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
                             <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="PluginAPI.family_list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI.family_list">[docs]</a>    <span class="k">def</span> <span class="nf">family_list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the list of plugin families.</span>

<span class="sd">        :sc-api:`plugin-families: list &lt;Plugin-Family.html#PluginFamilyRESTReference-/pluginFamily&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">            filter (tuple, optional):</span>
<span class="sd">                A filter tuple for which to filter the plugins.  Filter tuples</span>
<span class="sd">                must be ``(&#39;name&#39;, &#39;operator&#39;, &#39;value&#39;)`` and follow a similar</span>
<span class="sd">                yet different format to the analysis filters.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of plugins to return.  Available types are ``active``,</span>
<span class="sd">                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and</span>
<span class="sd">                ``passive``.  If nothing is specified, then ``all`` is assumed.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of plugin family records.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for fam in sc.plugins.family_list():</span>
<span class="sd">            ...     pprint(fam)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pluginFamily&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">query</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="PluginAPI.family_details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI.family_details">[docs]</a>    <span class="k">def</span> <span class="nf">family_details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for the specified plugin family.</span>

<span class="sd">        :sc-api:`plugin-family: details &lt;https://docs.tenable.com/sccv/api/Plugin-Family.html#PluginFamilyRESTReference-/pluginFamily/{id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            plugin_id (int): The plugin family numeric identifier.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The plugin family resource.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; family = sc.plugins.family_details(10)</span>
<span class="sd">            &gt;&gt;&gt; pprint(family)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                                         <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pluginFamily/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="PluginAPI.family_plugins"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.plugins.PluginAPI.family_plugins">[docs]</a>    <span class="k">def</span> <span class="nf">family_plugins</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the plugins for the specified family.</span>

<span class="sd">        :sc-api:`plugin-family: plugins &lt;Plugin-Family.html#PluginFamilyRESTReference-/pluginFamily/{id}/plugins::GET&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            plugin_id (int): The numeric identifier for the plugin family.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">            filter (tuple, optional):</span>
<span class="sd">                A filter tuple for which to filter the plugins.  Filter tuples</span>
<span class="sd">                must be ``(&#39;name&#39;, &#39;operator&#39;, &#39;value&#39;)`` and follow a similar</span>
<span class="sd">                yet different format to the analysis filters.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                How many records should be returned in each page of data.  If</span>
<span class="sd">                none is specified, the default is 1000 records.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                At what offset within the data should we start returning data.</span>
<span class="sd">                If none is specified, the default is 0.</span>
<span class="sd">            pages (int, optional):</span>
<span class="sd">                How many pages of data should we return.  If none is specified</span>
<span class="sd">                then all pages will return.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field to sort the results on.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort the results.  Valid settings are</span>
<span class="sd">                ``asc`` and ``desc``.  The default is ``asc``.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of plugins to return.  Available types are ``active``,</span>
<span class="sd">                ``all``, ``compliance``, ``custom``, ``lce``, ``notPassive``, and</span>
<span class="sd">                ``passive``.  If nothing is specified, then ``all`` is assumed.</span>

<span class="sd">        Returns:</span>
<span class="sd">            PluginResultsIterator: an iterator object handling data pagination.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; plugins = sc.plugins.family_plugins(10)</span>
<span class="sd">            &gt;&gt;&gt; for plugin in plugins:</span>
<span class="sd">            ...     pprint(plugin)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">offset</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="mi">0</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">limit</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="mi">1000</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">pages</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">,</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;pages&#39;</span><span class="p">),</span> <span class="nb">int</span><span class="p">)</span>
        <span class="n">json_result</span> <span class="o">=</span> <span class="n">kwargs</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;json_result&#39;</span><span class="p">,</span> <span class="kc">False</span><span class="p">)</span>
        <span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kwargs</span><span class="p">)</span>

        <span class="k">if</span> <span class="n">json_result</span><span class="p">:</span>
            <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;plugin&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">query</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span>
        <span class="k">return</span> <span class="n">PluginResultsIterator</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="p">,</span>
                                         <span class="n">_resource</span><span class="o">=</span><span class="s1">&#39;pluginFamily/</span><span class="si">{}</span><span class="s1">/plugins&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
                                             <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;plugin_id&#39;</span><span class="p">,</span> <span class="n">plugin_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
                                         <span class="n">_offset</span><span class="o">=</span><span class="n">offset</span><span class="p">,</span>
                                         <span class="n">_limit</span><span class="o">=</span><span class="n">limit</span><span class="p">,</span>
                                         <span class="n">_query</span><span class="o">=</span><span class="n">query</span><span class="p">,</span>
                                         <span class="n">_pages_total</span><span class="o">=</span><span class="n">pages</span><span class="p">)</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.plugins</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
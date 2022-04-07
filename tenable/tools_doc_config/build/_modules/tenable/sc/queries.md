
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.queries &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.queries</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.queries</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Queries</span>
<span class="sd">=======</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Query &lt;Query.html&gt;` API.  These items are typically seen</span>
<span class="sd">under the **Workflow -&gt; Query** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.queries``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: QueryAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>

<div class="viewcode-block" id="QueryAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI">[docs]</a><span class="k">class</span> <span class="nc">QueryAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a query definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">query</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_query_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="n">kw</span> <span class="o">=</span> <span class="n">dict_merge</span><span class="p">(</span><span class="n">kw</span><span class="p">,</span> <span class="n">query</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;query&#39;</span><span class="p">,</span> <span class="nb">dict</span><span class="p">()))</span>

        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;tags&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tags&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tags&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;sort_field&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sortField&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_field&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;sort_direction&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sortDir&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;sort_direction&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_direction&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ASC&#39;</span><span class="p">,</span> <span class="s1">&#39;DESC&#39;</span><span class="p">],</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_direction&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;offset&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;offset&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;offset&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;offset&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;limit&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;limit&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;limit&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;limit&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;owner_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ownerID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;owner_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;owner_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">))</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;owner_id&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;context&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;context&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;context&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;browse_cols&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browseColumns&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;browse_cols&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_cols&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">))</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_cols&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;browse_sort_col&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browseSortColumn&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;browse_sort_col&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_sort_col&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_sort_col&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;browse_sort_direction&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browseSortDirection&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;browse_sort_direction&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_sort_direction&#39;</span><span class="p">],</span>
                <span class="nb">str</span><span class="p">,</span> <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ASC&#39;</span><span class="p">,</span> <span class="s1">&#39;DESC&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;browse_sort_direction&#39;</span><span class="p">])</span>

        <span class="k">return</span> <span class="n">kw</span>


<div class="viewcode-block" id="QueryAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">tool</span><span class="p">,</span> <span class="n">data_type</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a query.</span>

<span class="sd">        :sc-api:`query: create &lt;Query.html#query_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of the new query</span>
<span class="sd">            tool (str):</span>
<span class="sd">                The tool to use to query the data.</span>
<span class="sd">            data_type (str):</span>
<span class="sd">                The type of data to query.</span>
<span class="sd">            *filters (tuple, optional):</span>
<span class="sd">                The filters to use for the query.  Refer to the documentation</span>
<span class="sd">                within the :ref:&#39;tenable.sc.analysis&#39; for more information on</span>
<span class="sd">                how to construct these.</span>
<span class="sd">            browse_cols (list, optional):</span>
<span class="sd">                What columns are set to be browsable for the analysis view.</span>
<span class="sd">            browse_sort_col (str, optional):</span>
<span class="sd">                The browsable column in which to sort on.</span>
<span class="sd">            browse_sort_dir (str, optional):</span>
<span class="sd">                The direction in which to sort.  Valid values are ``asc`` and</span>
<span class="sd">                ``desc``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description for the query.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                The limit to the number of records to return.  If nothing is</span>
<span class="sd">                specified, the API defaults to 100 records.</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                The number of records to skip before returning results.  If</span>
<span class="sd">                nothing is specified, then the default is 0.</span>
<span class="sd">            owner_id (int, optional):</span>
<span class="sd">                The identifier stating the owner of the query.  If left</span>
<span class="sd">                unspecified, then the default is the current user.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort.  Valid values are ``asc`` and</span>
<span class="sd">                ``desc``.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field in which to sort the results.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                Tags definition for the query.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created query.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; query = sc.queries.create(&#39;New Query&#39;, &#39;vulndetails&#39;, &#39;vuln&#39;,</span>
<span class="sd">            ...     (&#39;pluginID&#39;, &#39;=&#39;, &#39;19506&#39;))</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">tool</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">data_type</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;query&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific query.</span>

<span class="sd">        :sc-api:`query: details &lt;Query.html#QueryRESTReference-/query/{id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the query.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The query resource record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; query = sc.queries.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(query)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;query/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a query.</span>

<span class="sd">        :sc-api:`query: edit &lt;Query.html#query_id_PATCH&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            *filters (tuple, optional):</span>
<span class="sd">                The filters to use for the query.  Refer to the documentation</span>
<span class="sd">                within the :ref:&#39;tenable.sc.analysis&#39; for more information on</span>
<span class="sd">                how to construct these.</span>
<span class="sd">            browse_cols (str, optional):</span>
<span class="sd">                What columns are set to be browsable for the analysis view.</span>
<span class="sd">            browse_sort_col (list, optional):</span>
<span class="sd">                The browsable column in which to sort on.</span>
<span class="sd">            browse_sort_dir (str, optional):</span>
<span class="sd">                The direction in which to sort.  Valid values are ``asc`` and</span>
<span class="sd">                ``desc``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description for the query.</span>
<span class="sd">            limit (int, optional):</span>
<span class="sd">                The limit to the number of records to return.  If nothing is</span>
<span class="sd">                specified, the API defaults to 100 records.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name of the new query</span>
<span class="sd">            offset (int, optional):</span>
<span class="sd">                The number of records to skip before returning results.  If</span>
<span class="sd">                nothing is specified, then the default is 0.</span>
<span class="sd">            owner_id (int, optional):</span>
<span class="sd">                The identifier stating the owner of the query.  If left</span>
<span class="sd">                unspecified, then the default is the current user.</span>
<span class="sd">            sort_direction (str, optional):</span>
<span class="sd">                The direction in which to sort.  Valid values are ``asc`` and</span>
<span class="sd">                ``desc``.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                The field in which to sort the results.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                Tags definition for the query.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                The tool to use to query the data.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of data to query.</span>
<span class="sd">        Returns:</span>
<span class="sd">           :obj:` dict`:</span>
<span class="sd">                The newly updated query.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; query = sc.queries.edit()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">*</span><span class="n">filters</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;query/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a query.</span>

<span class="sd">        :sc-api:`query: delete &lt;Query.html#query_id_DELETE&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the query to remove.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.queries.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;query/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of query definitions.</span>

<span class="sd">        :sc-api:`query: list &lt;Query.html#QueryRESTReference-/query&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each query.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of query resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for query in sc.queries.list():</span>
<span class="sd">            ...     pprint(query)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;query&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.share"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.share">[docs]</a>    <span class="k">def</span> <span class="nf">share</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">groups</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Shares the specified query to another user group.</span>

<span class="sd">        :sc-api:`query: share &lt;Query.html#QueryRESTReference-/query/{id}/share&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric id for the query.</span>
<span class="sd">            *groups (int): The numeric id of the group(s) to share to.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated query resource.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.queries.share(1, group_1, group_2)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;query/</span><span class="si">{}</span><span class="s1">/share&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;groups&#39;</span><span class="p">:</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">groups</span><span class="p">]})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="QueryAPI.tags"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.queries.QueryAPI.tags">[docs]</a>    <span class="k">def</span> <span class="nf">tags</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of unique tags associated to queries.</span>

<span class="sd">        :sc-api:`query: tags &lt;Query.html#QueryRESTReference-/query/tag&gt;`</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of tags</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tags = sc.queries.tags()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;query/tag&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.queries</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
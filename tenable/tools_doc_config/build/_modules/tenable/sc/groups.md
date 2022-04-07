
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.groups &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.groups</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.groups</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Groups</span>
<span class="sd">======</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Group &lt;Group.html&gt;` API.  These items are typically seen under the</span>
<span class="sd">**User Groups** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.groups``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: GroupAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>

<div class="viewcode-block" id="GroupAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI">[docs]</a><span class="k">class</span> <span class="nc">GroupAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a group definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="n">mapping</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;viewable&#39;</span><span class="p">:</span> <span class="s1">&#39;definingAssets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;repos&#39;</span><span class="p">:</span> <span class="s1">&#39;repositories&#39;</span><span class="p">,</span>
            <span class="s1">&#39;lce_ids&#39;</span><span class="p">:</span> <span class="s1">&#39;lces&#39;</span><span class="p">,</span>
            <span class="s1">&#39;asset_lists&#39;</span><span class="p">:</span> <span class="s1">&#39;assets&#39;</span><span class="p">,</span>
            <span class="s1">&#39;scan_policies&#39;</span><span class="p">:</span> <span class="s1">&#39;policies&#39;</span><span class="p">,</span>
            <span class="s1">&#39;query_ids&#39;</span><span class="p">:</span> <span class="s1">&#39;queries&#39;</span><span class="p">,</span>
            <span class="s1">&#39;scan_creds&#39;</span><span class="p">:</span> <span class="s1">&#39;credentials&#39;</span><span class="p">,</span>
            <span class="s1">&#39;dashboards&#39;</span><span class="p">:</span> <span class="s1">&#39;dashboardTabs&#39;</span><span class="p">,</span>
            <span class="s1">&#39;report_cards&#39;</span><span class="p">:</span> <span class="s1">&#39;arcs&#39;</span><span class="p">,</span>
            <span class="s1">&#39;audit_files&#39;</span><span class="p">:</span> <span class="s1">&#39;auditFiles&#39;</span>
        <span class="p">}</span>
        <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">v</span> <span class="ow">in</span> <span class="n">mapping</span><span class="o">.</span><span class="n">items</span><span class="p">():</span>
            <span class="k">if</span> <span class="n">k</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
                <span class="c1"># For each item in the mapping, expand the kwarg if it exists</span>
                <span class="c1"># into a list of dictionaries with an id attribute.  Associate</span>
                <span class="c1"># the expanded list to the value of the hash table and delete</span>
                <span class="c1"># the original kwarg.</span>
                <span class="n">kw</span><span class="p">[</span><span class="n">v</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;</span><span class="si">{}</span><span class="s1">:item&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">k</span><span class="p">),</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="n">k</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="n">k</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
                <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="n">k</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>

<div class="viewcode-block" id="GroupAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a group.</span>

<span class="sd">        :sc-api:`group: create &lt;Group.html#group_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str): The name of the user group</span>
<span class="sd">            asset_lists (list, optional):</span>
<span class="sd">                List of asset list ids to allow this group to access.</span>
<span class="sd">            audit_files (list, optional):</span>
<span class="sd">                List of audit file ids to allow this group to access.</span>
<span class="sd">            dashboards (list, optional):</span>
<span class="sd">                List of dashboard ids to allow this group to access.</span>
<span class="sd">            lce_ids (list, optional):</span>
<span class="sd">                List of LCE ionstance ids to allow this group to access.</span>
<span class="sd">            query_ids (list, optional):</span>
<span class="sd">                List of query ids to allow this group to access.</span>
<span class="sd">            report_cards (list, optional):</span>
<span class="sd">                List of report card ids to allow this group to access.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                List of repository ids to allow this group to access.</span>
<span class="sd">            scan_creds (list, optional):</span>
<span class="sd">                List of scanning credential ids to allow this group to access.</span>
<span class="sd">            scan_policies (list, optional):</span>
<span class="sd">                List of scan policy ids to allow this group to access.</span>
<span class="sd">            viewable (list, optional):</span>
<span class="sd">                List of asset list ids to use for the purposes of restricting</span>
<span class="sd">                what members of this group can see within Tenable.sc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created group.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; group = sc.groups.create(&#39;New Group&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;group&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="GroupAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific group.</span>

<span class="sd">        :sc-api:`group: details &lt;Group.html#GroupRESTReference-/group/{id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the group.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The group resource record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; group = sc.groups.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(group)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;group/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="GroupAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a group.</span>

<span class="sd">        :sc-api:`group: edit &lt;Group.html#group_id_PATCH&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            asset_lists (list, optional):</span>
<span class="sd">                List of asset list ids to allow this group to access.</span>
<span class="sd">            audit_files (list, optional):</span>
<span class="sd">                List of audit file ids to allow this group to access.</span>
<span class="sd">            dashboards (list, optional):</span>
<span class="sd">                List of dashboard ids to allow this group to access.</span>
<span class="sd">            lce_ids (list, optional):</span>
<span class="sd">                List of LCE ionstance ids to allow this group to access.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name of the user group</span>
<span class="sd">            query_ids (list, optional):</span>
<span class="sd">                List of query ids to allow this group to access.</span>
<span class="sd">            report_cards (list, optional):</span>
<span class="sd">                List of report card ids to allow this group to access.</span>
<span class="sd">            repos (list, optional):</span>
<span class="sd">                List of repository ids to allow this group to access.</span>
<span class="sd">            scan_creds (list, optional):</span>
<span class="sd">                List of scanning credential ids to allow this group to access.</span>
<span class="sd">            scan_policies (list, optional):</span>
<span class="sd">                List of scan policy ids to allow this group to access.</span>
<span class="sd">            viewable (list, optional):</span>
<span class="sd">                List of asset list ids to use for the purposes of restricting</span>
<span class="sd">                what members of this group can see within Tenable.sc.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated group.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; group = sc.groups.edit()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;group/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="GroupAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a group.</span>

<span class="sd">        :sc-api:`group: delete &lt;Group.html#group_id_DELETE&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the group to remove.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.groups.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;group/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="GroupAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.groups.GroupAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of group definitions.</span>

<span class="sd">        :sc-api:`group: list &lt;Group.html#group_GET&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each group.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of group resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for group in sc.groups.list():</span>
<span class="sd">            ...     pprint(group)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;group&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.groups</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="index" title="Index" href="../../../../genindex.md" />
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.widget.api</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.widget.api</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Widget</span>
<span class="sd">=======</span>
<span class="sd">Methods described in this section relate to the widget API.</span>
<span class="sd">These methods can be accessed at ``TenableAD.widgets``.</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: WidgetsAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">List</span><span class="p">,</span> <span class="n">Dict</span>
<span class="kn">from</span> <span class="nn">tenable.ad.widget.schema</span> <span class="kn">import</span> <span class="n">WidgetSchema</span><span class="p">,</span> <span class="n">WidgetOptionSchema</span>
<span class="kn">from</span> <span class="nn">tenable.base.endpoint</span> <span class="kn">import</span> <span class="n">APIEndpoint</span>
<div class="viewcode-block" id="WidgetsAPI"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI">[docs]</a><span class="k">class</span> <span class="nc">WidgetsAPI</span><span class="p">(</span><span class="n">APIEndpoint</span><span class="p">):</span>
    <span class="n">_path</span> <span class="o">=</span> <span class="s1">&#39;dashboards&#39;</span>
    <span class="n">_schema</span> <span class="o">=</span> <span class="n">WidgetSchema</span><span class="p">()</span>
<div class="viewcode-block" id="WidgetsAPI.list"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves all the widgets.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            list:</span>
<span class="sd">                The list of widget objects.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.list(dashboard_id=13)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">/widgets&quot;</span><span class="p">)</span></div>
<div class="viewcode-block" id="WidgetsAPI.create"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">pos_x</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">pos_y</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">width</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">height</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">title</span><span class="p">:</span> <span class="nb">str</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a new widget.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            pos_x (int):</span>
<span class="sd">                x-axis position for widget.</span>
<span class="sd">            pos_y (int):</span>
<span class="sd">                y-axis position for widget.</span>
<span class="sd">            width (int):</span>
<span class="sd">                width of widget.</span>
<span class="sd">            height (int):</span>
<span class="sd">                height of widget.</span>
<span class="sd">            title (str):</span>
<span class="sd">                title for widget.</span>
<span class="sd">        Returns:</span>
<span class="sd">            list[dict]:</span>
<span class="sd">                The created widget object.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.create(</span>
<span class="sd">            ...     dashboard_id=1,</span>
<span class="sd">            ...     pos_x=1,</span>
<span class="sd">            ...     pos_y=1,</span>
<span class="sd">            ...     width=2,</span>
<span class="sd">            ...     height=2,</span>
<span class="sd">            ...     title=&#39;ExampleWidget&#39;,</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;posX&#39;</span><span class="p">:</span> <span class="n">pos_x</span><span class="p">,</span>
            <span class="s1">&#39;posY&#39;</span><span class="p">:</span> <span class="n">pos_y</span><span class="p">,</span>
            <span class="s1">&#39;width&#39;</span><span class="p">:</span> <span class="n">width</span><span class="p">,</span>
            <span class="s1">&#39;height&#39;</span><span class="p">:</span> <span class="n">height</span><span class="p">,</span>
            <span class="s1">&#39;title&#39;</span><span class="p">:</span> <span class="n">title</span>
        <span class="p">}))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_post</span><span class="p">(</span><span class="sa">f</span><span class="s1">&#39;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s1">/widgets&#39;</span><span class="p">,</span>
                                            <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>
<div class="viewcode-block" id="WidgetsAPI.details"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
                <span class="n">widget_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for a specific widget.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            widget_id (int):</span>
<span class="sd">                The widget instance identifier</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The widget object.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widget.details(dashboard_id=1, widget_id=1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">&quot;</span>
                                           <span class="sa">f</span><span class="s2">&quot;/widgets/</span><span class="si">{</span><span class="n">widget_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">))</span></div>
<div class="viewcode-block" id="WidgetsAPI.update"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.update">[docs]</a>    <span class="k">def</span> <span class="nf">update</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">widget_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Updates an existing widget.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            widget_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            pos_x (optional, int):</span>
<span class="sd">                x-axis position for widget.</span>
<span class="sd">            pos_y (optional, int):</span>
<span class="sd">                y-axis position for widget.</span>
<span class="sd">            width (optional, int):</span>
<span class="sd">                width of widget.</span>
<span class="sd">            height (optional, int):</span>
<span class="sd">                height of widget.</span>
<span class="sd">            title (optional, str):</span>
<span class="sd">                title for widget.</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The updated widget object.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.update(</span>
<span class="sd">            ...     dashboard_id=1,</span>
<span class="sd">            ...     widget_id=1,</span>
<span class="sd">            ...     pos_x=1,</span>
<span class="sd">            ...     pos_y=1,</span>
<span class="sd">            ...     width=3,</span>
<span class="sd">            ...     height=3,</span>
<span class="sd">            ...     title=&#39;EditedWidget&#39;</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">kwargs</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_patch</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">&quot;</span>
                                             <span class="sa">f</span><span class="s2">&quot;/widgets/</span><span class="si">{</span><span class="n">widget_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">,</span>
                                             <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">))</span></div>
<div class="viewcode-block" id="WidgetsAPI.delete"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
               <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
               <span class="n">widget_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Deletes an existing widget.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            widget_id (int):</span>
<span class="sd">                The widget instance identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            None:</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.delete(</span>
<span class="sd">            ...     dashboard_id=1,</span>
<span class="sd">            ...     widget_id=1</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_delete</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">/widgets/</span><span class="si">{</span><span class="n">widget_id</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span></div>
<div class="viewcode-block" id="WidgetsAPI.widget_options_details"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.widget_options_details">[docs]</a>    <span class="k">def</span> <span class="nf">widget_options_details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                               <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
                               <span class="n">widget_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="n">Dict</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Gets the details of widget options.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            widget_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">        Returns:</span>
<span class="sd">            dict:</span>
<span class="sd">                The widget option object.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.widget_options_details(</span>
<span class="sd">            ...     widget_id=1,</span>
<span class="sd">            ...     dashboard_id=1</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">WidgetOptionSchema</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_get</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">/widgets/&quot;</span>
                                     <span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">widget_id</span><span class="si">}</span><span class="s2">/options&quot;</span><span class="p">))</span></div>
<div class="viewcode-block" id="WidgetsAPI.define_widget_options"><a class="viewcode-back" href="../../../../tenable.ad.widget.md#tenable.ad.widget.api.WidgetsAPI.define_widget_options">[docs]</a>    <span class="k">def</span> <span class="nf">define_widget_options</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span>
                              <span class="n">dashboard_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
                              <span class="n">widget_id</span><span class="p">:</span> <span class="nb">int</span><span class="p">,</span>
                              <span class="n">chart_type</span><span class="p">:</span> <span class="nb">str</span><span class="p">,</span>
                              <span class="n">series</span><span class="p">:</span> <span class="n">List</span><span class="p">[</span><span class="n">Dict</span><span class="p">]</span>
                              <span class="p">)</span> <span class="o">-&gt;</span> <span class="kc">None</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Defines the widget option.</span>
<span class="sd">        Args:</span>
<span class="sd">            dashboard_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            widget_id (int):</span>
<span class="sd">                The dashboard instance identifier.</span>
<span class="sd">            chart_type (str):</span>
<span class="sd">                The type of chart for widget. possible options</span>
<span class="sd">                 are ``BigNumber``, ``LineChart``, ``BarChart``,</span>
<span class="sd">                 ``SecurityCompliance`` and ``StepChart``.</span>
<span class="sd">            series (list):</span>
<span class="sd">                Additional keywords passed will be added to the series</span>
<span class="sd">                list of dicts within the API call.</span>
<span class="sd">        Returns:</span>
<span class="sd">            None:</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tad.widgets.define_widget_options(</span>
<span class="sd">            ...     dashboard_id=1,</span>
<span class="sd">            ...     widget_id=1,</span>
<span class="sd">            ...     chart_type=&#39;BigNumber&#39;</span>
<span class="sd">            ...     series=[</span>
<span class="sd">            ...     {</span>
<span class="sd">            ...         &#39;dataOptions&#39;: {</span>
<span class="sd">            ...             &#39;type&#39;: &#39;User&#39;,</span>
<span class="sd">            ...             &#39;duration&#39;: 1,</span>
<span class="sd">            ...             &#39;directoryIds&#39;: [1, 2, 3],</span>
<span class="sd">            ...             &#39;active&#39;: True</span>
<span class="sd">            ...         },</span>
<span class="sd">            ...         &#39;displayOptions&#39;: {</span>
<span class="sd">            ...             &#39;label&#39;: &#39;label&#39;</span>
<span class="sd">            ...         }</span>
<span class="sd">            ...     }</span>
<span class="sd">            ...     ]</span>
<span class="sd">            ...     )</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">schema</span> <span class="o">=</span> <span class="n">WidgetOptionSchema</span><span class="p">()</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="n">schema</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">schema</span><span class="o">.</span><span class="n">load</span><span class="p">({</span>
            <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="n">chart_type</span><span class="p">,</span>
            <span class="s1">&#39;series&#39;</span><span class="p">:</span> <span class="nb">list</span><span class="p">(</span><span class="n">series</span><span class="p">)</span>
        <span class="p">}))</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_put</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="n">dashboard_id</span><span class="si">}</span><span class="s2">/widgets/</span><span class="si">{</span><span class="n">widget_id</span><span class="si">}</span><span class="s2">/options&quot;</span><span class="p">,</span>
                  <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span></div></div>
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
          <a href="../../../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../../../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.ad.widget.api</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
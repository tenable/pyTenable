
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.asset_lists &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.asset_lists</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.asset_lists</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Asset Lists</span>
<span class="sd">===========</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Assets &lt;Asset.html&gt;` API.  These items are typically seen</span>
<span class="sd">under the **Assets** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.asset_lists``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AssetListAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">UnexpectedValueError</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>

<div class="viewcode-block" id="AssetListAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI">[docs]</a><span class="k">class</span> <span class="nc">AssetListAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_dynamic_rules_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">rule</span><span class="p">,</span> <span class="n">sub</span><span class="o">=</span><span class="kc">False</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles expanding the tuple format into the JSON formatted request.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">rule</span><span class="p">,</span> <span class="nb">dict</span><span class="p">):</span>
            <span class="c1"># if the rule is a dictionary, then simply pass it through as-is.</span>
            <span class="k">return</span> <span class="n">rule</span>
        <span class="k">elif</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">rule</span><span class="p">,</span> <span class="nb">tuple</span><span class="p">):</span>
            <span class="c1"># if the rule is a tuple, then we will want to convert it into the</span>
            <span class="c1"># expected dictionary format.</span>
            <span class="k">if</span> <span class="n">rule</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;all&#39;</span><span class="p">,</span> <span class="s1">&#39;any&#39;</span><span class="p">]:</span>
                <span class="c1"># if the first parameter in the tuple is either &quot;any&quot; or &quot;all&quot;,</span>
                <span class="c1"># we will then assume that this is a group of rules, and call</span>
                <span class="c1"># the rule constructor for every subsequent parameter in the</span>
                <span class="c1"># tuple.</span>
                <span class="n">resp</span> <span class="o">=</span> <span class="p">{</span>
                    <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="n">rule</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span>
                    <span class="s1">&#39;children&#39;</span><span class="p">:</span> <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_dynamic_rules_constructor</span><span class="p">(</span><span class="n">r</span><span class="p">,</span> <span class="n">sub</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
                        <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="n">rule</span><span class="p">[</span><span class="mi">1</span><span class="p">:]]</span>
                <span class="p">}</span>
                <span class="k">if</span> <span class="n">sub</span><span class="p">:</span>
                    <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;group&#39;</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="c1"># as the first item was _not_ &quot;all&quot; or &quot;any&quot;, we&#39;re safe to</span>
                <span class="c1"># assume that the rule is actually a rule clause.  In this case</span>
                <span class="c1"># we will want to validate the fields based on the potential</span>
                <span class="c1"># known values that each attribute could have.  The rule should</span>
                <span class="c1"># generally be constructed in the following format:</span>
                <span class="c1">#</span>
                <span class="c1"># (&#39;filterName&#39;, &#39;operator&#39;, &#39;value&#39;)</span>
                <span class="c1">#</span>
                <span class="c1"># or in the case of a plugin constraint, then there will be a</span>
                <span class="c1"># fourth parameter like so:</span>
                <span class="c1">#</span>
                <span class="c1"># (&#39;filterName&#39;, &#39;operator&#39;, &#39;value&#39;, int(pluginID))</span>
                <span class="c1"># or</span>
                <span class="c1"># (&#39;filterName&#39;, &#39;operator&#39;, &#39;value&#39;, list(id1, id2, id3, etc.))</span>
                <span class="n">resp</span> <span class="o">=</span> <span class="p">{</span>
                    <span class="s1">&#39;type&#39;</span><span class="p">:</span> <span class="s1">&#39;clause&#39;</span><span class="p">,</span>
                    <span class="s1">&#39;filterName&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;rule:name&#39;</span><span class="p">,</span> <span class="n">rule</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                        <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;dns&#39;</span><span class="p">,</span> <span class="s1">&#39;exploitAvailable&#39;</span><span class="p">,</span> <span class="s1">&#39;exploitFrameworks&#39;</span><span class="p">,</span>
                            <span class="s1">&#39;firstseen&#39;</span><span class="p">,</span> <span class="s1">&#39;mac&#39;</span><span class="p">,</span> <span class="s1">&#39;os&#39;</span><span class="p">,</span> <span class="s1">&#39;ip&#39;</span><span class="p">,</span> <span class="s1">&#39;uuid&#39;</span><span class="p">,</span> <span class="s1">&#39;lastseen&#39;</span><span class="p">,</span>
                            <span class="s1">&#39;netbioshost&#39;</span><span class="p">,</span> <span class="s1">&#39;netbiosworkgroup&#39;</span><span class="p">,</span> <span class="s1">&#39;pluginid&#39;</span><span class="p">,</span>
                            <span class="s1">&#39;plugintext&#39;</span><span class="p">,</span> <span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="s1">&#39;severity&#39;</span><span class="p">,</span> <span class="s1">&#39;sshv1&#39;</span><span class="p">,</span> <span class="s1">&#39;sshv2&#39;</span><span class="p">,</span>
                            <span class="s1">&#39;tcpport&#39;</span><span class="p">,</span> <span class="s1">&#39;udpport&#39;</span><span class="p">,</span> <span class="s1">&#39;xref&#39;</span><span class="p">]),</span>
                    <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;rule:operator&#39;</span><span class="p">,</span> <span class="n">rule</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                        <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;contains&#39;</span><span class="p">,</span> <span class="s1">&#39;eq&#39;</span><span class="p">,</span> <span class="s1">&#39;lt&#39;</span><span class="p">,</span> <span class="s1">&#39;lte&#39;</span><span class="p">,</span> <span class="s1">&#39;ne&#39;</span><span class="p">,</span> <span class="s1">&#39;gt&#39;</span><span class="p">,</span>
                            <span class="s1">&#39;gte&#39;</span><span class="p">,</span> <span class="s1">&#39;regex&#39;</span><span class="p">,</span> <span class="s1">&#39;pcre&#39;</span><span class="p">])</span>
                <span class="p">}</span>

                <span class="c1"># if the value is an integer, then we will want to ensure that</span>
                <span class="c1"># we wrap the value within an id dictionary.  This is necessary</span>
                <span class="c1"># for pluginid and severity filter names.  In all other cases</span>
                <span class="c1"># the value should be a string.</span>
                <span class="k">if</span> <span class="n">rule</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;pluginid&#39;</span><span class="p">,</span> <span class="s1">&#39;severity&#39;</span><span class="p">]:</span>
                    <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
                        <span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;rule:value&#39;</span><span class="p">,</span> <span class="n">rule</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">else</span><span class="p">:</span>
                    <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;value&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;rule:value&#39;</span><span class="p">,</span> <span class="n">rule</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

                <span class="c1"># if there is a plugin constraint, then we will want to convert</span>
                <span class="c1"># the plugin constraint into a string value.  If it&#39;s a single</span>
                <span class="c1"># plugin id, then we will simply convert from int to str.  If</span>
                <span class="c1"># a list of values is provided, then we will build a comma-delim</span>
                <span class="c1"># string with the values that were passed.</span>
                <span class="k">if</span> <span class="nb">len</span><span class="p">(</span><span class="n">rule</span><span class="p">)</span> <span class="o">==</span> <span class="mi">4</span><span class="p">:</span>
                    <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">rule</span><span class="p">[</span><span class="mi">3</span><span class="p">],</span> <span class="nb">int</span><span class="p">):</span>
                        <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;pluginIDConstraint&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="n">rule</span><span class="p">[</span><span class="mi">3</span><span class="p">])</span>
                    <span class="k">elif</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">rule</span><span class="p">[</span><span class="mi">3</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                        <span class="n">resp</span><span class="p">[</span><span class="s1">&#39;pluginIDConstraint&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span>
                            <span class="p">[</span><span class="nb">str</span><span class="p">(</span><span class="n">r</span><span class="p">)</span> <span class="k">for</span> <span class="n">r</span> <span class="ow">in</span> <span class="n">rule</span><span class="p">[</span><span class="mi">3</span><span class="p">]])</span>
                    <span class="k">else</span><span class="p">:</span>
                        <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span>
                            <span class="s1">&#39;rule </span><span class="si">{}</span><span class="s1"> has an invalid plugin constraint.&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">rule</span><span class="p">))</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s1">&#39;rules </span><span class="si">{}</span><span class="s1"> not a tuple or dict&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="n">rule</span><span class="p">))</span>
        <span class="k">return</span> <span class="n">resp</span>

    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a asset-list definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># ensure that they type is a string and is one of the valid values.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span>
                <span class="s1">&#39;combination&#39;</span><span class="p">,</span> <span class="s1">&#39;dnsname&#39;</span><span class="p">,</span> <span class="s1">&#39;dnsnameupload&#39;</span><span class="p">,</span> <span class="s1">&#39;dynamic&#39;</span><span class="p">,</span>
                <span class="s1">&#39;ldapquery&#39;</span><span class="p">,</span> <span class="s1">&#39;static&#39;</span><span class="p">,</span> <span class="s1">&#39;staticeventfilter&#39;</span><span class="p">,</span> <span class="s1">&#39;staticvulnfilter&#39;</span><span class="p">,</span>
                <span class="s1">&#39;templates&#39;</span><span class="p">,</span> <span class="s1">&#39;upload&#39;</span><span class="p">,</span> <span class="s1">&#39;watchlist&#39;</span><span class="p">,</span> <span class="s1">&#39;watchlisteventfilter&#39;</span><span class="p">,</span>
                <span class="s1">&#39;watchlistupload&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;prep&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># ensure that prep is a boolean value and store the string equiv in</span>
            <span class="c1"># the prepare parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;prepare&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;prep&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;prep&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;prep&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the name param is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the description param is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;context&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the context param is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;context&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;context&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;tags&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the tags param is a string</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tags&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tags&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;template&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if the template param is an integer then convert it into a dict</span>
            <span class="c1"># with the integer value stored in the id attribute.  If the</span>
            <span class="c1"># template attribute is a dictionary, then we will simply assume</span>
            <span class="c1"># that the information is what we want to pass and allow through.</span>
            <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;template&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;template&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;filename&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the filename is a string value</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filename&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;fobj&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Uploads the file object and stores the returned name in filename.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;fobj&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;fobj&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;data_fields&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the data_fields parameter is a list and store it</span>
            <span class="c1"># within the assetDataFields attribute.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;assetDataFields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;data_fields&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_fields&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_fields&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;combinations&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if the combinations parameter is a tuple, then send the value to</span>
            <span class="c1"># the combo_expansion method to convert the tuple to the dictionary</span>
            <span class="c1"># equivalent.  If the value is a dictionary, then simply pass the</span>
            <span class="c1"># value as-is.</span>
            <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;combinations&#39;</span><span class="p">],</span> <span class="nb">tuple</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;combinations&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_combo_expansion</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;combinations&#39;</span><span class="p">])</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;combinations&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;combinations&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;rules&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># pass the rules parameter to the dynamic rules constructor to</span>
            <span class="c1"># convert the rules from a tuple to an expanded dictionary or just</span>
            <span class="c1"># pass through the dictionary value if presented with a dict.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;rules&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_dynamic_rules_constructor</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;rules&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;dns_names&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate the dns_names parameter is a list or str value and store</span>
            <span class="c1"># it within the definedDNSNames attribute.</span>
            <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dns_names&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;definedDNSNames&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span>
                    <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;dns:item&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dns_names&#39;</span><span class="p">]])</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;definedDNSNames&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                    <span class="s1">&#39;dns_names&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dns_names&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dns_names&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;dn&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="s1">&#39;search_string&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="s1">&#39;ldap_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># if the dn, search_string, and ldap_id attributes are all defined,</span>
            <span class="c1"># then construct the definedLDAPQuery sub-document with these fields</span>
            <span class="c1"># and validate that they are the appropriate types.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;definedLDAPQuery&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span>
                <span class="s1">&#39;searchBase&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;dn&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dn&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">),</span>
                <span class="s1">&#39;searchString&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                    <span class="s1">&#39;search_string&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;search_string&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">),</span>
                <span class="s1">&#39;ldap&#39;</span><span class="p">:</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="p">}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dn&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;search_string&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">])</span>
        <span class="k">elif</span> <span class="p">((</span><span class="s1">&#39;dn&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="p">(</span><span class="s1">&#39;search_string&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">or</span> <span class="s1">&#39;ldap_id&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">))</span>
          <span class="ow">or</span> <span class="p">(</span><span class="s1">&#39;search_string&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="p">(</span><span class="s1">&#39;dn&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">or</span> <span class="s1">&#39;ldap_id&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">))</span>
          <span class="ow">or</span> <span class="p">(</span><span class="s1">&#39;ldap_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">and</span> <span class="p">(</span><span class="s1">&#39;search_string&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span> <span class="ow">or</span> <span class="s1">&#39;dn&#39;</span> <span class="ow">not</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">))):</span>
            <span class="k">raise</span> <span class="n">UnexpectedValueError</span><span class="p">(</span>
                <span class="s1">&#39;dn, search_string, and ldap_id must all be present&#39;</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;ips&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that ips is either a list or a string value and store the</span>
            <span class="c1"># value as a comma-seperated string in definedIPs</span>
            <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;definedIPs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ips:item&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">]])</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;definedIPs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ips&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ips&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;exclude_managed_ips&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that exclude managed ips is a boolean value and store the</span>
            <span class="c1"># value as a string in excludeManagedIPs</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;excludeManagedIPs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;exclude_managed_ips&#39;</span><span class="p">,</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;exclude_managed_ips&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;exclude_managed_ips&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;filters&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate the filters attribute is a list.  For each item, we will</span>
            <span class="c1"># want to convert any tuples to the expanded dictionaries and simply</span>
            <span class="c1"># pass through any dictionaries.</span>
            <span class="n">flist</span> <span class="o">=</span> <span class="nb">list</span><span class="p">()</span>
            <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filters&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filters&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                <span class="k">if</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">f</span><span class="p">,</span> <span class="nb">tuple</span><span class="p">):</span>
                    <span class="n">flist</span><span class="o">.</span><span class="n">append</span><span class="p">({</span>
                        <span class="s1">&#39;filterName&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:name&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="nb">str</span><span class="p">),</span>
                        <span class="s1">&#39;operator&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:operator&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">[</span><span class="mi">1</span><span class="p">],</span> <span class="nb">str</span><span class="p">),</span>
                        <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter:value&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">[</span><span class="mi">2</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
                    <span class="p">})</span>
                <span class="k">else</span><span class="p">:</span>
                    <span class="n">flist</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filter&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">dict</span><span class="p">))</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filters&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">flist</span>

        <span class="k">if</span> <span class="s1">&#39;tool&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the tools attribute is a string,</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;tool&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tool&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;source_type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the source_type parameter is a string and store it</span>
            <span class="c1"># within the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sourceType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;source_type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;source_type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;source_type&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;start_offset&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate the start offset is an integer value and store it within</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;startOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;start_offset&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;start_offset&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;start_offset&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;end_offset&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the end offset is an integer value and store it</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;endOffset&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;end_offset&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;end_offset&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;end_offset&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;view&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the view is a string value.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;view&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;view&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>

        <span class="k">if</span> <span class="s1">&#39;lce_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the lce_id is an integer value and store it as a</span>
            <span class="c1"># dictionary within the lce attribute.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lce&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;lce_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lce_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;lce_id&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;sort_field&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that sort_field is a string value and store within the</span>
            <span class="c1"># camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sortField&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;sort_field&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_field&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;sort_dir&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that sort_dir is a string value of either ASC or DESC and</span>
            <span class="c1"># store it within the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sortDir&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;sort_dir&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_dir&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">case</span><span class="o">=</span><span class="s1">&#39;upper&#39;</span><span class="p">,</span> <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;ASC&#39;</span><span class="p">,</span> <span class="s1">&#39;DESC&#39;</span><span class="p">])</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;sort_dir&#39;</span><span class="p">])</span>

        <span class="k">if</span> <span class="s1">&#39;scan_id&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate that the scan_id value is an integer and store it within</span>
            <span class="c1"># the camelCase equiv.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scanID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;scan_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_id&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;scan_id&#39;</span><span class="p">])</span>

        <span class="k">return</span> <span class="n">kw</span>

<div class="viewcode-block" id="AssetListAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">list_type</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates an asset-list.</span>

<span class="sd">        :sc-api:`asset-list: create &lt;Asset.html#asset_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name for the asset list to create.</span>
<span class="sd">            list_type (str):</span>
<span class="sd">                The type of list to create.  Supported values are</span>
<span class="sd">                ``combination``, ``dnsname``, ``dnsnameupload``, ``dynamic``,</span>
<span class="sd">                ``ldapquery``, ``static``, ``staticeventfilter``,</span>
<span class="sd">                ``staticvulnfilter``, ``templates``, ``upload``, ``watchlist``,</span>
<span class="sd">                ``watchlisteventfilter``, and ``watchlistupload``.</span>
<span class="sd">            combinations (tuple, optional):</span>
<span class="sd">                An asset combination tuple.  For further information refer to</span>
<span class="sd">                the asset combination logic described at</span>
<span class="sd">                :mod:`tenable.sc.analysis`.</span>
<span class="sd">            data_fields (list, optional):</span>
<span class="sd">                A list of data fields as required for a given asset list type.</span>
<span class="sd">                Each item within the list should be formatted in the following</span>
<span class="sd">                way: ``{&#39;fieldName&#39;: &#39;name&#39;, &#39;fieldValue&#39;: &#39;value&#39;}``</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description for the asset list being created.</span>
<span class="sd">            dn (str, optional):</span>
<span class="sd">                The base DN to use for an LDAP query.  Must also provide a</span>
<span class="sd">                ``search_string`` and an ``ldap_id``.</span>
<span class="sd">            dns_names (list, optional):</span>
<span class="sd">                When defining a DNS asset list, use this attribute to provide</span>
<span class="sd">                the list of DNS addresses.</span>
<span class="sd">            exclude_managed_ips (bool, optional):</span>
<span class="sd">                Determines whether or not managed IPs should be excluded from</span>
<span class="sd">                the asset list.</span>
<span class="sd">            filters (list, optional):</span>
<span class="sd">                A list of filter tuples to use when defining filtered asset</span>
<span class="sd">                list types.  Follows the same format as filters within the rest</span>
<span class="sd">                of pyTenable.</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                A file-like object to use when uploading an asset list.</span>
<span class="sd">            ips (list, optional):</span>
<span class="sd">                A list of IP Addresses, CIDRs, and/or IP Address ranges to use</span>
<span class="sd">                for the purposes of a static asset list.</span>
<span class="sd">            lce_id (int, optional):</span>
<span class="sd">                When defining a event-based asset list, which LCE should be used</span>
<span class="sd">                to generate the asset list query.</span>
<span class="sd">            ldap_id (int, optional):</span>
<span class="sd">                The numeric identifier pertaining to the LDAP server to use for</span>
<span class="sd">                an LDAP query.  must also provide a ``dn`` and a</span>
<span class="sd">                ``search_string``.</span>
<span class="sd">            prep (bool, optional):</span>
<span class="sd">                Should asset preparation be run after the list is created?  If</span>
<span class="sd">                unspecified, the default action is ``True``.</span>
<span class="sd">            rules (tuple, optional):</span>
<span class="sd">                For a dynamic asset list, the tuple definition of the rules to</span>
<span class="sd">                determine what Ips are associated to this asset list.  Rules</span>
<span class="sd">                follow a similar pattern to the asset combination logic and</span>
<span class="sd">                are written in a way to follow the same visual methodology as</span>
<span class="sd">                the UI.</span>

<span class="sd">                For example, a simple dynamic ruleset may look like:</span>

<span class="sd">                .. code-block:: python</span>

<span class="sd">                    (&#39;any&#39;, (&#39;dns&#39;, &#39;contains&#39;, &#39;svc.company.tld&#39;),</span>
<span class="sd">                            (&#39;dns&#39;, &#39;contains&#39;, &#39;prod.company.tld&#39;))</span>

<span class="sd">                Which would match all assets with either svc.company.tld or</span>
<span class="sd">                prod.company.tld in their DNS names.  Rule gropups can be nested</span>
<span class="sd">                as well, by supplying a new group tuple instead of a rule:</span>

<span class="sd">                .. code-block:: python</span>

<span class="sd">                    (&#39;any&#39;, (&#39;dns&#39;, &#39;contains&#39;, &#39;svc.company.tld&#39;),</span>
<span class="sd">                            (&#39;dns&#39;, &#39;contains&#39;, &#39;prod.company.tld&#39;),</span>
<span class="sd">                            (&#39;any&#39;, (&#39;ip&#39;, &#39;contains&#39;, &#39;192.168.140&#39;),</span>
<span class="sd">                                    (&#39;ip&#39;, &#39;contains&#39;, &#39;192.168.141&#39;)))</span>

<span class="sd">                In this example we have nested another group requiring that the</span>
<span class="sd">                ip may contain either of the values in addition to any of the</span>
<span class="sd">                DNS rules.</span>

<span class="sd">                It&#39;s also possible to constrain the rule to a specific plugin or</span>
<span class="sd">                plugins as well by adding a 4th element in a rule tuple.</span>
<span class="sd">                Defining them would look like so:</span>

<span class="sd">                .. code-block:: python</span>

<span class="sd">                    # Singular Plugin ID</span>
<span class="sd">                    (&#39;plugintext&#39;, &#39;contains&#39;, &#39;credentialed&#39;, 19506)</span>
<span class="sd">                    # Multiple Plugin IDs</span>
<span class="sd">                    (&#39;plugintext&#39;, &#39;contains&#39;, &#39;stuff&#39;, [19506, 10180])</span>

<span class="sd">                * Available rules are ``dns``, ``exploitAvailable``,</span>
<span class="sd">                  ``exploitFrameworks``, ``firstseen``, ``mac``, ``os``, ``ip``,</span>
<span class="sd">                  ``uuid``, ``lastseen``, ``netbioshost``, ``netbiosworkgroup``,</span>
<span class="sd">                  ``pluginid``, ``plugintext``, ``port``, ``severity``, ``sshv1``,</span>
<span class="sd">                  ``sshv2``, ``tcpport``, ``udpport``, and ``xref``.</span>
<span class="sd">                * Available operators are ``contains``, ``eq``, ``lt``, ``lte``,</span>
<span class="sd">                  ``ne``, ``gt``, ``gte``, ``regex``, ``pcre``.</span>
<span class="sd">                * Group alauses are either ``any`` or ``all``.  Any is a logical</span>
<span class="sd">                  or.  All is a logical and.</span>
<span class="sd">            scan_id (int, optional):</span>
<span class="sd">                When defining an &quot;individual&quot; source_type, the numeric id of the</span>
<span class="sd">                scan instance to base the query upon.</span>
<span class="sd">            search_string (str, optional):</span>
<span class="sd">                The search string to use as part of an LDAP Query.  Must also</span>
<span class="sd">                provide a ``dn`` and an ``ldap_id``.</span>
<span class="sd">            sort_dir (str, optional):</span>
<span class="sd">                When defining a filtered asset list type, determines the</span>
<span class="sd">                direction of the sort to use.  This field must be passed when</span>
<span class="sd">                defining a sort_field.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                When defining a filtered asset list type, determines what field</span>
<span class="sd">                to sort the resulting query on.</span>
<span class="sd">            source_type (str, optional):</span>
<span class="sd">                The source of the data to query from when defining a filtered</span>
<span class="sd">                asset list type.</span>
<span class="sd">            start_offset (int, optional):</span>
<span class="sd">                The start offset of the filter to use when defining a filtered</span>
<span class="sd">                asset list type.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                A tag to associate to the asset list.</span>
<span class="sd">            template (int, optional):</span>
<span class="sd">                The numeric id of the template to use.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                When specifying filtered asset list types, the analysis tool to</span>
<span class="sd">                use for determining what IPs should be included within the</span>
<span class="sd">                asset list.</span>
<span class="sd">            view (str, optional):</span>
<span class="sd">                When the source_type is &quot;individual&quot;, the view defined what</span>
<span class="sd">                subset of the data to use.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The newly created asset-list.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; asset-list = sc.asset_lists.create()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">list_type</span>

        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;asset&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">org_id</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific asset-list.</span>

<span class="sd">        :sc-api:`asset-list: details&lt;Asset.html#AssetRESTReference-/asset/{id}?orgID={org_id}&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the asset-list.</span>
<span class="sd">            org_id (int, optional): The organizationID for the asset-list.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The details of asset id.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; asset_id_details = sc.asset_lists.details(1,1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(asset_id_details)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">if</span> <span class="n">org_id</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;orgID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">org_id</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span><span class="nb">int</span><span class="p">)),</span><span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits an asset-list.</span>

<span class="sd">        :sc-api:`asset-list: edit &lt;Asset.html#asset_id_PATCH&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int):</span>
<span class="sd">                The numeric id of the asset list to edit.</span>
<span class="sd">            combinations (tuple, optional):</span>
<span class="sd">                An asset combination tuple.  For further information refer to</span>
<span class="sd">                the asset combination logic described at</span>
<span class="sd">                :mod:`tenable.sc.analysis`.</span>
<span class="sd">            data_fields (list, optional):</span>
<span class="sd">                A list of data fields as required for a given asset list type.</span>
<span class="sd">                Each item within the list should be formatted in the following</span>
<span class="sd">                way: ``{&#39;fieldName&#39;: &#39;name&#39;, &#39;fieldValue&#39;: &#39;value&#39;}``</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description for the asset list being created.</span>
<span class="sd">            dn (str, optional):</span>
<span class="sd">                The base DN to use for an LDAP query.  Must also provide a</span>
<span class="sd">                ``search_string`` and an ``ldap_id``.</span>
<span class="sd">            dns_names (list, optional):</span>
<span class="sd">                When defining a DNS asset list, use this attribute to provide</span>
<span class="sd">                the list of DNS addresses.</span>
<span class="sd">            exclude_managed_ips (bool, optional):</span>
<span class="sd">                Determines whether or not managed IPs should be excluded from</span>
<span class="sd">                the asset list.</span>
<span class="sd">            filters (list, optional):</span>
<span class="sd">                A list of filter tuples to use when defining filtered asset</span>
<span class="sd">                list types.  Follows the same format as filters within the rest</span>
<span class="sd">                of pyTenable.</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                A file-like object to use when uploading an asset list.</span>
<span class="sd">            ips (list, optional):</span>
<span class="sd">                A list of IP Addresses, CIDRs, and/or IP Address ranges to use</span>
<span class="sd">                for the purposes of a static asset list.</span>
<span class="sd">            lce_id (int, optional):</span>
<span class="sd">                When defining a event-based asset list, which LCE should be used</span>
<span class="sd">                to generate the asset list query.</span>
<span class="sd">            ldap_id (int, optional):</span>
<span class="sd">                The numeric identifier pertaining to the LDAP server to use for</span>
<span class="sd">                an LDAP query.  must also provide a ``dn`` and a</span>
<span class="sd">                ``search_string``.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name for the asset list to create.</span>
<span class="sd">            prep (bool, optional):</span>
<span class="sd">                Should asset preparation be run after the list is created?  If</span>
<span class="sd">                unspecified, the default action is ``True``.</span>
<span class="sd">            rules (tuple, optional):</span>
<span class="sd">                For a dynamic asset list, the tuple definition of the rules to</span>
<span class="sd">                determine what Ips are associated to this asset list.  Rules</span>
<span class="sd">                follow a similar pattern to the asset combination logic and</span>
<span class="sd">                are written in a way to follow the same visual methodology as</span>
<span class="sd">                the UI.</span>
<span class="sd">            scan_id (int, optional):</span>
<span class="sd">                When defining an &quot;individual&quot; source_type, the numeric id of the</span>
<span class="sd">                scan instance to base the query upon.</span>
<span class="sd">            search_string (str, optional):</span>
<span class="sd">                The search string to use as part of an LDAP Query.  Must also</span>
<span class="sd">                provide a ``dn`` and an ``ldap_id``.</span>
<span class="sd">            sort_dir (str, optional):</span>
<span class="sd">                When defining a filtered asset list type, determines the</span>
<span class="sd">                direction of the sort to use.  This field must be passed when</span>
<span class="sd">                defining a sort_field.</span>
<span class="sd">            sort_field (str, optional):</span>
<span class="sd">                When defining a filtered asset list type, determines what field</span>
<span class="sd">                to sort the resulting query on.</span>
<span class="sd">            source_type (str, optional):</span>
<span class="sd">                The source of the data to query from when defining a filtered</span>
<span class="sd">                asset list type.</span>
<span class="sd">            start_offset (int, optional):</span>
<span class="sd">                The start offset of the filter to use when defining a filtered</span>
<span class="sd">                asset list type.</span>
<span class="sd">            tags (str, optional):</span>
<span class="sd">                A tag to associate to the asset list.</span>
<span class="sd">            template (int, optional):</span>
<span class="sd">                The numeric id of the template to use.</span>
<span class="sd">            tool (str, optional):</span>
<span class="sd">                When specifying filtered asset list types, the analysis tool to</span>
<span class="sd">                use for determining what IPs should be included within the</span>
<span class="sd">                asset list.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of list to create.  Supported values are</span>
<span class="sd">                ``combination``, ``dnsname``, ``dnsnameupload``, ``dynamic``,</span>
<span class="sd">                ``ldapquery``, ``static``, ``staticeventfilter``,</span>
<span class="sd">                ``staticvulnfilter``, ``templates``, ``upload``, ``watchlist``,</span>
<span class="sd">                ``watchlisteventfilter``, and ``watchlistupload``.</span>
<span class="sd">            view (str, optional):</span>
<span class="sd">                When the source_type is &quot;individual&quot;, the view defined what</span>
<span class="sd">                subset of the data to use.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The newly updated asset-list.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; asset-list = sc.asset_lists.edit()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a asset-list.</span>

<span class="sd">        :sc-api:`asset-list: delete &lt;Asset.html#asset_id_DELETE&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the asset-list to remove.</span>

<span class="sd">        Returns:</span>
<span class="sd">            dict: The deletion response dict</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.asset_lists.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of asset list definitions.</span>

<span class="sd">        :sc-api:`asset-list: list &lt;Asset.html#AssetRESTReference-/asset&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each asset-list.</span>

<span class="sd">        Returns:</span>
<span class="sd">            list: A list of asset-list resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for asset-list in sc.asset_lists.list():</span>
<span class="sd">            ...     pprint(asset-list)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;asset&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.import_definition"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.import_definition">[docs]</a>    <span class="k">def</span> <span class="nf">import_definition</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fobj</span><span class="p">,</span> <span class="n">name</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Imports an asset list definition from an asset list definition XML file.</span>

<span class="sd">        :sc-api:`asset-list: import &lt;Asset.html#asset_import_POST&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            name (str): The name of the asset definition to create.</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file-like object containing the XML definition.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The created asset list from the import.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example.xml&#39;, &#39;rb&#39;) as fobj:</span>
<span class="sd">            ...     sc.asset_lists.import_definition(&#39;Example&#39;, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;filename&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">fobj</span><span class="p">)}</span>
        <span class="k">if</span> <span class="n">name</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;asset/import&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.export_definition"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.export_definition">[docs]</a>    <span class="k">def</span> <span class="nf">export_definition</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Exports an asset list definition and stored the data in the file-like</span>
<span class="sd">        object that was passed.</span>

<span class="sd">        :sc-api:`asset-list: export &lt;Asset.html#AssetRESTReference-/asset/{id}/export&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the asset list to export.</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file-like object to store the asset list XML definition.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`FileObject`:</span>
<span class="sd">                The file-like object containing the XML definition.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example.xml&#39;, &#39;wb&#39;) as fobj:</span>
<span class="sd">            ...     sc.asset_lists.export_definition(1, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">/export&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

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

<div class="viewcode-block" id="AssetListAPI.refresh"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.refresh">[docs]</a>    <span class="k">def</span> <span class="nf">refresh</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="o">*</span><span class="n">repos</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Initiates an on-demand recalculation of the asset list.  Note this</span>
<span class="sd">        endpoint requires being logged in as an admin user.</span>

<span class="sd">        :sc-api:`asset-list: refresh &lt;Asset.html#AssetRESTReference-/asset/{id}/refresh&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier of the asset list to refresh.</span>
<span class="sd">            org_id (int): The organization associated to the asset list.</span>
<span class="sd">            *repos (int): Repository ids to perform the recalculation on.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                Response of the items that the asset list is associated to.</span>

<span class="sd">        Examples:</span>
<span class="sd">            Perform the refresh against a single repo:</span>

<span class="sd">            &gt;&gt;&gt; sc.asset_lists.refresh(1, 1, 1)</span>

<span class="sd">            Perform the refresh against many repos:</span>

<span class="sd">            &gt;&gt;&gt; sc.asset_lists.refresh(1, 1, 1, 2, 3)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">/refresh&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;orgID&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;org_id&#39;</span><span class="p">,</span> <span class="n">org_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">),</span>
                <span class="s1">&#39;repIDs&#39;</span><span class="p">:</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;repo:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">repos</span><span class="p">]</span>
            <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.ldap_query"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.ldap_query">[docs]</a>    <span class="k">def</span> <span class="nf">ldap_query</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">ldap_id</span><span class="p">,</span> <span class="n">dn</span><span class="p">,</span> <span class="n">search_string</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Performs a LDAP test query on the specified LDAP service configured.</span>

<span class="sd">        :sc-api:`asset-list: test-ldap-query &lt;Asset.html#AssetRESTReference-/asset/testLDAPQuery&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            ldap_id (int):</span>
<span class="sd">                The numeric identifier for the configured LDAP service.</span>
<span class="sd">            dn (str): The valid search base to use.</span>
<span class="sd">            search_string(str):</span>
<span class="sd">                The search string to query the LDAP service with.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The LDAP response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; resp = sc.asset_lists.ldap_query(1, &#39;domain.com&#39;, &#39;*&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;asset/testLDAPQuery&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;definedLDAPQuery&#39;</span><span class="p">:</span> <span class="p">{</span>
                <span class="s1">&#39;searchBase&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;dn&#39;</span><span class="p">,</span> <span class="n">dn</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
                <span class="s1">&#39;searchString&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;search_string&#39;</span><span class="p">,</span> <span class="n">search_string</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
                <span class="s1">&#39;ldap&#39;</span><span class="p">:</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;ldap_id&#39;</span><span class="p">,</span> <span class="n">ldap_id</span><span class="p">,</span> <span class="nb">int</span><span class="p">))}</span>
            <span class="p">}})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.tags"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.tags">[docs]</a>    <span class="k">def</span> <span class="nf">tags</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of unique tags associated to asset lists.</span>

<span class="sd">        :sc-api:`asset-lists: tags &lt;Asset.html#AssetRESTReference-/asset/tag&gt;`</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of tags</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tags = sc.asset_lists.tags()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;asset/tag&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="AssetListAPI.share"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.asset_lists.AssetListAPI.share">[docs]</a>    <span class="k">def</span> <span class="nf">share</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">groups</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Shares the specified asset list to another user group.</span>

<span class="sd">        :sc-api:`asset-lists: share &lt;Asset.html#AssetRESTReference-/asset/{id}/share&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric id for the credential.</span>
<span class="sd">            *groups (int): The numeric id of the group(s) to share to.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The updated asset-list resource.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.asset_lists.share(1, group_1, group_2)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;asset/</span><span class="si">{}</span><span class="s1">/share&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;groups&#39;</span><span class="p">:</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;group:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">groups</span><span class="p">]})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.asset_lists</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
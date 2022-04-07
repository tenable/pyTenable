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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scanners</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.scanners</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Scanners</span>
<span class="sd">========</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Scanner &lt;Scanner.html&gt;` API.  These items are typically seen under the</span>
<span class="sd">**Scanners** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.scanners``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScannerAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<div class="viewcode-block" id="ScannerAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI">[docs]</a><span class="k">class</span> <span class="nc">ScannerAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a scanner definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the name parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the description parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="c1"># Make sure that the appropriate authentication  type is set.</span>
        <span class="k">if</span> <span class="s1">&#39;username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;authType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;password&#39;</span>
        <span class="k">elif</span> <span class="s1">&#39;cert&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;authType&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;certificate&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;cert&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the cert parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;cert&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;cert&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;username&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the username parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;username&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;username&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;password&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the password parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;password&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;password&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;address&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the address parameter is a string and store it</span>
            <span class="c1"># within the ip parameter</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;ip&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;address&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;address&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;address&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;port&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the port parameter is a integer.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;proxy&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the proxy parameter is a boolean flag and store it</span>
            <span class="c1"># as a lowercased string in useProxy.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;useProxy&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;proxy&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;proxy&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;proxy&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;verify&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the verify parameter is a boolean flag and store it</span>
            <span class="c1"># as a lowercased string in verifyHost.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;verifyHost&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;verify&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;verify&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;verify&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;enabled&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the enabled parameter is a boolean flag and store it</span>
            <span class="c1"># as a lowercased string.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;enabled&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;enabled&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;enabled&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="k">if</span> <span class="s1">&#39;managed&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the managed parameter is a boolean flag and store it</span>
            <span class="c1"># as a lowercased string in managedPlugins.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managedPlugins&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;managed&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;managed&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;agent_capable&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the agent_capable parameter is a boolean flag and</span>
            <span class="c1"># store it as a lowercased string in agentCapable.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;agentCapable&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="nb">str</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;agent_capable&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;agent_capable&#39;</span><span class="p">],</span> <span class="nb">bool</span><span class="p">))</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;agent_capable&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;zone_ids&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the zone_ids parameter is a list and expand it to</span>
            <span class="c1"># list of dictionaries with the id attribute set to each of the</span>
            <span class="c1"># scan zone integer ids.  Store this in the zones parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;zones&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;zone:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;zone_id&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;zone_ids&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;zone_ids&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;orgs&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the orgs parameter is a list and expand it into a</span>
            <span class="c1"># list of dictionaries with the id attribute set to each of the</span>
            <span class="c1"># organization integer ids.  Store this in the nessusManagerOrgs</span>
            <span class="c1"># parameter.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;nessusManagerOrgs&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;orgs:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;orgs&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">],</span> <span class="nb">list</span><span class="p">)]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orgs&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="ScannerAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">address</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a scanner.</span>
<span class="sd">        :sc-api:`scanner: create &lt;Scanner.html#scanner_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            address (str): The address of the scanner</span>
<span class="sd">            name (str): The name of the scanner</span>
<span class="sd">            agent_capable (bool, optional):</span>
<span class="sd">                Is this scanner an agent capable scanner?  If left unspecified</span>
<span class="sd">                the default is ``False``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description of the scanner.</span>
<span class="sd">            enabled (bool, optional):</span>
<span class="sd">                Is this scanner enabled?  If left unspecified, the default is</span>
<span class="sd">                ``True``.</span>
<span class="sd">            managed (bool, optional):</span>
<span class="sd">                Is the plugin set for this scanner managed?  If left unspecified</span>
<span class="sd">                then the default is ``False``.</span>
<span class="sd">            orgs (list, optional):</span>
<span class="sd">                If the scanner is an agent capable scanner, then a list of</span>
<span class="sd">                organization ids is to be specified to attach the scanner for</span>
<span class="sd">                the purposes of agent scanning.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                What is the port that the Nessus service is running on.  If left</span>
<span class="sd">                unspecified, then the default is ``8834``.</span>
<span class="sd">            proxy (bool, optional):</span>
<span class="sd">                Is this scanner behind a proxy?  If left unspecified then the</span>
<span class="sd">                default is ``False``.</span>
<span class="sd">            zone_ids (list, optional):</span>
<span class="sd">                List of scan zones that this scanner is to be a member of.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created scanner.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; scanner = sc.scanners.create(&#39;Example Scanner&#39;, &#39;192.168.0.1&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="p">{</span>
            <span class="s1">&#39;port&#39;</span><span class="p">:</span> <span class="mi">8834</span><span class="p">,</span>
            <span class="s1">&#39;proxy&#39;</span><span class="p">:</span> <span class="kc">False</span><span class="p">,</span>
            <span class="s1">&#39;verify&#39;</span><span class="p">:</span> <span class="kc">False</span><span class="p">,</span>
            <span class="s1">&#39;enabled&#39;</span><span class="p">:</span> <span class="kc">True</span><span class="p">,</span>
            <span class="s1">&#39;managed&#39;</span><span class="p">:</span> <span class="kc">False</span><span class="p">,</span>
            <span class="s1">&#39;agent_capable&#39;</span><span class="p">:</span> <span class="kc">False</span><span class="p">,</span>
            <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="n">name</span><span class="p">,</span>
            <span class="s1">&#39;address&#39;</span><span class="p">:</span> <span class="n">address</span><span class="p">,</span>
        <span class="p">}</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">dict_merge</span><span class="p">(</span><span class="n">payload</span><span class="p">,</span> <span class="n">kw</span><span class="p">))</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanner&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific scanner.</span>
<span class="sd">        :sc-api:`scanner: details &lt;Scanner.html#scanner_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the scanner.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scanner resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; scanner = sc.scanners.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(scanner)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scanner/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a scanner.</span>
<span class="sd">        :sc-api:`scanner: edit &lt;Scanner.html#scanner_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the scanner.</span>
<span class="sd">            address (str, optional): The address of the scanner</span>
<span class="sd">            agent_capable (bool, optional):</span>
<span class="sd">                Is this scanner an agent capable scanner?  If left unspecified</span>
<span class="sd">                the default is ``False``.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                The description of the scanner.</span>
<span class="sd">            enabled (bool, optional):</span>
<span class="sd">                Is this scanner enabled?  If left unspecified, the default is</span>
<span class="sd">                ``True``.</span>
<span class="sd">            managed (bool, optional):</span>
<span class="sd">                Is the plugin set for this scanner managed?  If left unspecified</span>
<span class="sd">                then the default is ``False``.</span>
<span class="sd">            name (str, optional): The name of the scanner</span>
<span class="sd">            orgs (list, optional):</span>
<span class="sd">                If the scanner is an agent capable scanner, then a list of</span>
<span class="sd">                organization ids is to be specified to attach the scanner for</span>
<span class="sd">                the purposes of agent scanning.</span>
<span class="sd">            port (int, optional):</span>
<span class="sd">                What is the port that the Nessus service is running on.  If left</span>
<span class="sd">                unspecified, then the default is ``8834``.</span>
<span class="sd">            proxy (bool, optional):</span>
<span class="sd">                Is this scanner behind a proxy?  If left unspecified then the</span>
<span class="sd">                default is ``False``.</span>
<span class="sd">            zone_ids (list, optional):</span>
<span class="sd">                List of scan zones that this scanner is to be a member of.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated scanner.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; scanner = sc.scanners.edit(1, enabled=True)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;scanner/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="nb">id</span><span class="p">),</span>
            <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the specified scanner.</span>
<span class="sd">        :sc-api:`scanner: delete &lt;Scanner.html#scanner_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the scanner to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scanners.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;scanner/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of scanner definitions.</span>
<span class="sd">        :sc-api:`scanner: list &lt;Scanner.html#scanner_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each scanner.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of scanner resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for scanner in sc.scanners.list():</span>
<span class="sd">            ...     pprint(scanner)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scanner&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.agent_scans"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.agent_scans">[docs]</a>    <span class="k">def</span> <span class="nf">agent_scans</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">search</span><span class="p">,</span> <span class="n">results</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of agent scans that meed the specified search</span>
<span class="sd">        criteria.</span>
<span class="sd">        :sc-api:`scanner: test-scans-query &lt;Scanner.html#ScannerRESTReference-/scanner/{id}/testScansQuery&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric id of the scanner.</span>
<span class="sd">            search (str):</span>
<span class="sd">                The search string to send to the scanner.</span>
<span class="sd">            results (list, optonal):</span>
<span class="sd">                The list of results ids to test.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The list of scans that match the search criteria.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; scans = sc.scanners.agent_scans(&#39;*&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">(</span><span class="n">scansGlob</span><span class="o">=</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;search&#39;</span><span class="p">,</span> <span class="n">search</span><span class="p">,</span> <span class="nb">str</span><span class="p">))</span>
        <span class="k">if</span> <span class="n">results</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;resultsSync&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;results:id&#39;</span><span class="p">,</span> <span class="n">i</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span>
                <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;results&#39;</span><span class="p">,</span> <span class="n">results</span><span class="p">,</span> <span class="nb">list</span><span class="p">)]</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanner/</span><span class="si">{}</span><span class="s1">/testScansQuery&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="ScannerAPI.update_status"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scanners.ScannerAPI.update_status">[docs]</a>    <span class="k">def</span> <span class="nf">update_status</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Starts an on-demand scanner status update.</span>
<span class="sd">        :sc-api:`scanner: update-status &lt;Scanner.html#ScannerRESTReference-/scanner/updateStatus&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                The updated scanner status for all scanners.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; status = sc.scanners.update_status()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanner/updateStatus&#39;</span><span class="p">,</span>
            <span class="n">json</span><span class="o">=</span><span class="p">{})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;status&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scanners</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
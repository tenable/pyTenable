
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.reports.nessusv2 &#8212; pyTenable  documentation</title>
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
          <li class="nav-item nav-item-1"><a href="../../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.reports.nessusv2</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.reports.nessusv2</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">.. autoclass:: NessusReportv2</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">tenable.errors</span> <span class="kn">import</span> <span class="n">PackageMissingError</span>

<span class="k">try</span><span class="p">:</span>
    <span class="kn">from</span> <span class="nn">defusedxml.ElementTree</span> <span class="kn">import</span> <span class="n">iterparse</span>
<span class="k">except</span> <span class="ne">ImportError</span><span class="p">:</span>
    <span class="k">raise</span> <span class="n">PackageMissingError</span><span class="p">(</span>
        <span class="s1">&#39;The python package defusedxml is required for NessusReportv2&#39;</span><span class="p">)</span>

<span class="kn">import</span> <span class="nn">dateutil.parser</span><span class="o">,</span> <span class="nn">time</span>


<div class="viewcode-block" id="NessusReportv2"><a class="viewcode-back" href="../../../tenable.reports.md#tenable.reports.nessusv2.NessusReportv2">[docs]</a><span class="k">class</span> <span class="nc">NessusReportv2</span><span class="p">(</span><span class="nb">object</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    The NessusReportv2 generator will return vulnerability items from any</span>
<span class="sd">    Nessus version 2 formatted Nessus report file.  The returned data will be</span>
<span class="sd">    a python dictionary representation of the ReportItem with the relevant</span>
<span class="sd">    host properties attached.  The ReportItem&#39;s structure itself will determine</span>
<span class="sd">    the resulting dictionary, what attributes are returned, and what is not.</span>

<span class="sd">    Please note that in order to use this generator, you must install the python</span>
<span class="sd">    ``lxml`` package.</span>

<span class="sd">    Args:</span>
<span class="sd">        fobj (File object or string path):</span>
<span class="sd">            Either a File-like object or a string path pointing to the file to</span>
<span class="sd">            be parsed.</span>

<span class="sd">    Examples:</span>
<span class="sd">        For example, if we wanted to load a Nessus report from disk and iterate</span>
<span class="sd">        through the contents, it would simply be a matter of:</span>

<span class="sd">        &gt;&gt;&gt; with open(&#39;example.nessus&#39;) as nessus_file:</span>
<span class="sd">        ...     report = NessusReportv2(nessus_file)</span>
<span class="sd">        ...     for item in report:</span>
<span class="sd">        ...         print(item)</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="fm">__init__</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fobj</span><span class="p">):</span>
        <span class="bp">self</span><span class="o">.</span><span class="n">_iter</span> <span class="o">=</span> <span class="n">iterparse</span><span class="p">(</span><span class="n">fobj</span><span class="p">,</span> <span class="n">events</span><span class="o">=</span><span class="p">(</span><span class="s1">&#39;start&#39;</span><span class="p">,</span> <span class="s1">&#39;end&#39;</span><span class="p">))</span>

    <span class="k">def</span> <span class="fm">__iter__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span>

    <span class="k">def</span> <span class="fm">__next__</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">next</span><span class="p">()</span>

    <span class="k">def</span> <span class="nf">_defs</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">value</span><span class="p">):</span>
        <span class="k">if</span> <span class="n">name</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;cvss_vector&#39;</span><span class="p">,</span> <span class="s1">&#39;cvss_temporal_vector&#39;</span><span class="p">]:</span>
            <span class="c1"># Return a list of the Vectors instead of having everything in a</span>
            <span class="c1"># flat string.  This should allow for much easier parsing later.</span>
            <span class="k">return</span> <span class="n">value</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;/&#39;</span><span class="p">)</span>

        <span class="k">elif</span> <span class="n">name</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;cvss_base_score&#39;</span><span class="p">,</span> <span class="s1">&#39;cvss_temporal_score&#39;</span><span class="p">]:</span>
            <span class="c1"># CVSS scores are floats, so lets return them as such.</span>
            <span class="k">return</span> <span class="nb">float</span><span class="p">(</span><span class="n">value</span><span class="p">)</span>

        <span class="k">elif</span> <span class="n">name</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;first_found&#39;</span><span class="p">,</span> <span class="s1">&#39;last_found&#39;</span><span class="p">,</span> <span class="s1">&#39;plugin_modification_date&#39;</span><span class="p">,</span>
                      <span class="s1">&#39;plugin_publication_date&#39;</span><span class="p">,</span> <span class="s1">&#39;HOST_END&#39;</span><span class="p">,</span> <span class="s1">&#39;HOST_START&#39;</span><span class="p">]:</span>
            <span class="c1"># The first and last found attributes use a datetime timestamp</span>
            <span class="c1"># format that we should convert into a unix timestamp.</span>
            <span class="k">return</span> <span class="n">dateutil</span><span class="o">.</span><span class="n">parser</span><span class="o">.</span><span class="n">parse</span><span class="p">(</span><span class="n">value</span><span class="p">)</span>

        <span class="k">elif</span> <span class="n">name</span> <span class="ow">in</span> <span class="p">[</span><span class="s1">&#39;port&#39;</span><span class="p">,</span> <span class="s1">&#39;pluginID&#39;</span><span class="p">,</span> <span class="s1">&#39;severity&#39;</span><span class="p">]:</span>
            <span class="k">return</span> <span class="nb">int</span><span class="p">(</span><span class="n">value</span><span class="p">)</span>

        <span class="k">else</span><span class="p">:</span>
            <span class="k">return</span> <span class="n">value</span>

<div class="viewcode-block" id="NessusReportv2.next"><a class="viewcode-back" href="../../../tenable.reports.md#tenable.reports.nessusv2.NessusReportv2.next">[docs]</a>    <span class="k">def</span> <span class="nf">next</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Get the next ReportItem from the nessus file and return it as a</span>
<span class="sd">        python dictionary.</span>

<span class="sd">        Generally speaking this method is not called directly, but is instead</span>
<span class="sd">        called as part of a loop.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">try</span><span class="p">:</span>
            <span class="k">for</span> <span class="n">event</span><span class="p">,</span> <span class="n">elem</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_iter</span><span class="p">:</span>
                <span class="k">if</span> <span class="n">event</span> <span class="o">==</span> <span class="s1">&#39;start&#39;</span> <span class="ow">and</span> <span class="n">elem</span><span class="o">.</span><span class="n">tag</span> <span class="o">==</span> <span class="s1">&#39;ReportHost&#39;</span><span class="p">:</span>
                    <span class="c1"># If we detect a new ReportHost, then we will want to rebuild</span>
                    <span class="c1"># the host information cache, starting with the ReportHost&#39;s</span>
                    <span class="c1"># name for the host.</span>
                    <span class="bp">self</span><span class="o">.</span><span class="n">_cache</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;host-report-name&#39;</span><span class="p">:</span> <span class="n">elem</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">)}</span>

                <span class="k">if</span> <span class="n">event</span> <span class="o">==</span> <span class="s1">&#39;end&#39;</span> <span class="ow">and</span> <span class="n">elem</span><span class="o">.</span><span class="n">tag</span> <span class="o">==</span> <span class="s1">&#39;HostProperties&#39;</span><span class="p">:</span>
                    <span class="c1"># Once we have finished parsing out all of the host properties,</span>
                    <span class="c1"># we need to update the host cache with this new information.</span>
                    <span class="k">for</span> <span class="n">child</span> <span class="ow">in</span> <span class="n">elem</span><span class="p">:</span>
                        <span class="bp">self</span><span class="o">.</span><span class="n">_cache</span><span class="p">[</span><span class="n">child</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">)]</span> <span class="o">=</span> <span class="n">child</span><span class="o">.</span><span class="n">text</span>
                    <span class="n">elem</span><span class="o">.</span><span class="n">clear</span><span class="p">()</span>

                <span class="k">if</span> <span class="n">event</span> <span class="o">==</span> <span class="s1">&#39;end&#39;</span> <span class="ow">and</span> <span class="n">elem</span><span class="o">.</span><span class="n">tag</span> <span class="o">==</span> <span class="s1">&#39;ReportHost&#39;</span><span class="p">:</span>
                    <span class="c1"># If we reach the end of the ReportHost tree, then clear out</span>
                    <span class="c1"># the element.</span>
                    <span class="n">elem</span><span class="o">.</span><span class="n">clear</span><span class="p">()</span>
                <span class="k">if</span> <span class="n">event</span> <span class="o">==</span> <span class="s1">&#39;end&#39;</span> <span class="ow">and</span> <span class="n">elem</span><span class="o">.</span><span class="n">tag</span> <span class="o">==</span> <span class="s1">&#39;NessusClientData_v2&#39;</span><span class="p">:</span>
                    <span class="c1"># If we reach the end of the Nessus file, then we need to raise</span>
                    <span class="c1"># a StopIteration exception to inform the code downstream that</span>
                    <span class="c1"># we have reached the end of the file.</span>
                    <span class="k">raise</span> <span class="ne">StopIteration</span><span class="p">()</span>

                <span class="k">if</span> <span class="n">event</span> <span class="o">==</span> <span class="s1">&#39;end&#39;</span> <span class="ow">and</span> <span class="n">elem</span><span class="o">.</span><span class="n">tag</span> <span class="o">==</span> <span class="s1">&#39;ReportItem&#39;</span><span class="p">:</span>
                    <span class="c1"># Once we have finished gathering all of the information for a</span>
                    <span class="c1"># ReportItem, lets go ahead and parse out the ReportItem, graft</span>
                    <span class="c1"># on the cached HostProperties that we gathered before, and then</span>
                    <span class="c1"># return the data as a python dictionary.</span>
                    <span class="n">vuln</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">(</span><span class="n">elem</span><span class="o">.</span><span class="n">attrib</span><span class="p">)</span>
                    <span class="n">vuln</span><span class="o">.</span><span class="n">update</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_cache</span><span class="p">)</span>

                    <span class="c1"># all of the information we have passed into the vuln dictionary</span>
                    <span class="c1"># needs to be normalized.  Here we will pass each item through</span>
                    <span class="c1"># the definition parser to make sure any known values are</span>
                    <span class="c1"># formatted properly.</span>
                    <span class="k">for</span> <span class="n">k</span> <span class="ow">in</span> <span class="n">vuln</span><span class="o">.</span><span class="n">keys</span><span class="p">():</span>
                        <span class="n">vuln</span><span class="p">[</span><span class="n">k</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_defs</span><span class="p">(</span><span class="n">k</span><span class="p">,</span> <span class="n">vuln</span><span class="p">[</span><span class="n">k</span><span class="p">])</span>

                    <span class="k">for</span> <span class="n">c</span> <span class="ow">in</span> <span class="n">elem</span><span class="p">:</span>
                        <span class="c1"># iterate through each child element and add it to the vuln</span>
                        <span class="c1"># dictionary.  We will also check to see if we have seen</span>
                        <span class="c1"># the tag before, and if so, convert the stored value to a</span>
                        <span class="c1"># list of values.  The need to return a list is common for</span>
                        <span class="c1"># things like CVEs, BIDs, See-Alsos, etc.</span>

                        <span class="k">if</span> <span class="n">c</span><span class="o">.</span><span class="n">tag</span> <span class="ow">in</span> <span class="n">vuln</span><span class="p">:</span>
                            <span class="k">if</span> <span class="ow">not</span> <span class="nb">isinstance</span><span class="p">(</span><span class="n">vuln</span><span class="p">[</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">],</span> <span class="nb">list</span><span class="p">):</span>
                                <span class="n">vuln</span><span class="p">[</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">]</span> <span class="o">=</span> <span class="p">[</span><span class="n">vuln</span><span class="p">[</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">],]</span>
                            <span class="n">vuln</span><span class="p">[</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">]</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_defs</span><span class="p">(</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">,</span> <span class="n">c</span><span class="o">.</span><span class="n">text</span><span class="p">))</span>
                        <span class="k">else</span><span class="p">:</span>
                            <span class="n">vuln</span><span class="p">[</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_defs</span><span class="p">(</span><span class="n">c</span><span class="o">.</span><span class="n">tag</span><span class="p">,</span> <span class="n">c</span><span class="o">.</span><span class="n">text</span><span class="p">)</span>

                    <span class="c1"># Clear out the element from the element tree and return the</span>
                    <span class="c1"># vuln dictionary.</span>
                    <span class="n">elem</span><span class="o">.</span><span class="n">clear</span><span class="p">()</span>
                    <span class="k">return</span> <span class="n">vuln</span>
        <span class="k">except</span> <span class="ne">TypeError</span> <span class="k">as</span> <span class="n">err</span><span class="p">:</span>
            <span class="k">if</span> <span class="n">err</span><span class="o">.</span><span class="n">args</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="s1">&#39;reading file objects must return bytes objects&#39;</span><span class="p">:</span>
                <span class="k">raise</span> <span class="ne">TypeError</span><span class="p">(</span><span class="s1">&#39;File object not opened in binary mode.&#39;</span><span class="p">)</span>
            <span class="k">else</span><span class="p">:</span>
                <span class="k">raise</span> <span class="n">err</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.reports.nessusv2</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
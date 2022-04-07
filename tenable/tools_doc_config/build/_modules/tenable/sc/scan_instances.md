
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.scan_instances &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scan_instances</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.scan_instances</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Scan Instances</span>
<span class="sd">==============</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Scan Result &lt;Scan-Result.html&gt;` API.  While the Tenable.sc API refers</span>
<span class="sd">to the model these endpoints interact with as *ScanResult*, were actually</span>
<span class="sd">interacting with an instance of a scan definition stored within the *Scan* API</span>
<span class="sd">endpoints.  These scan instances could be running scans, stopped scans, errored</span>
<span class="sd">scans, or completed scans.  These items are typically seen under the</span>
<span class="sd">**Scan Results** section of Tenable.sc.</span>

<span class="sd">Methods available on ``sc.scan_instances``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: ScanResultAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">tenable.utils</span> <span class="kn">import</span> <span class="n">dict_merge</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>

<div class="viewcode-block" id="ScanResultAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI">[docs]</a><span class="k">class</span> <span class="nc">ScanResultAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
<div class="viewcode-block" id="ScanResultAPI.copy"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.copy">[docs]</a>    <span class="k">def</span> <span class="nf">copy</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">users</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Clones the scan instance.</span>

<span class="sd">        :sc-api:`scan-result: copy &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/copy&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier of the scan instance to clone.</span>
<span class="sd">            *users (int):</span>
<span class="sd">                A user id to associate to the scan instance.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The cloned scan instance record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.copy(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">users</span><span class="p">:</span>
            <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;users&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;user:id&#39;</span><span class="p">,</span> <span class="n">u</span><span class="p">,</span> <span class="nb">int</span><span class="p">)}</span> <span class="k">for</span> <span class="n">u</span> <span class="ow">in</span> <span class="n">users</span><span class="p">]</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/copy&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the scan instance from TenableSC.</span>

<span class="sd">        :sc-api:`scan-result: delete &lt;Scan-Result.html#scanResult_id_DELETE&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier of the scan instance to delete.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty string.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the details for the specified scan instance.</span>

<span class="sd">        :sc-api:`scan-result: details &lt;Scan-Result.html#scanResult_id_GET&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the scan instance to be retrieved.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                List of fields to return.  Refer to the API documentation</span>
<span class="sd">                referenced above for a list of available fields.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The scan instance resource record.</span>

<span class="sd">        Examples:</span>
<span class="sd">            Getting the details of a scan instance with just the</span>
<span class="sd">            default parameters:</span>

<span class="sd">            &gt;&gt;&gt; scan = sc.scan_instances.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(scan)</span>

<span class="sd">            Specifying what fields you&#39;d like to be returned:</span>

<span class="sd">            &gt;&gt;&gt; scan = sc.scan_instances.details(1,</span>
<span class="sd">            ...     fields=[&#39;name&#39;, &#39;status&#39;, &#39;scannedIPs&#39;, &#39;startTime&#39;, &#39;finishTime&#39;])</span>
<span class="sd">            &gt;&gt;&gt; pprint(scan)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;fields&#39;</span><span class="p">,</span> <span class="n">fields</span><span class="p">,</span> <span class="nb">list</span><span class="p">)])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.email"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.email">[docs]</a>    <span class="k">def</span> <span class="nf">email</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">*</span><span class="n">emails</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Emails the scan results of the requested scan to the email addresses</span>
<span class="sd">        defined.</span>

<span class="sd">        :sc-api:`scan-result: email &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/email&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the specified scan instance.</span>
<span class="sd">            *emails (str): Valid email address.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                Empty string response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.email(1, &#39;email@company.tld&#39;)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/email&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span><span class="s1">&#39;email&#39;</span><span class="p">:</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span>
                <span class="p">[</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;address&#39;</span><span class="p">,</span> <span class="n">e</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">e</span> <span class="ow">in</span> <span class="n">emails</span><span class="p">])})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.export_scan"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.export_scan">[docs]</a>    <span class="k">def</span> <span class="nf">export_scan</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">export_format</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Downloads the results of the scan.</span>

<span class="sd">        :sc-api:`scan-result: download &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/download&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The scan instance identifier.</span>
<span class="sd">            export_format (str, optional):</span>
<span class="sd">                The format of the resulting data.  Allowable values are</span>
<span class="sd">                ``scap1_2`` and ``v2``.  ``v2`` is the default value if none</span>
<span class="sd">                are specified.</span>
<span class="sd">            fobj (FileObject, optional):</span>
<span class="sd">                The file-like object to write the resulting file into.  If</span>
<span class="sd">                no file-like object is provided, a BytesIO objects with the</span>
<span class="sd">                downloaded file will be returned.  Be aware that the default</span>
<span class="sd">                option of using a BytesIO object means that the file will be</span>
<span class="sd">                stored in memory, and it&#39;s generally recommended to pass an</span>
<span class="sd">                actual file-object to write to instead.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`FileObject`:</span>
<span class="sd">                The file-like object with the resulting zipped report.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example.zip&#39;, &#39;wb&#39;) as fobj:</span>
<span class="sd">            ...     sc.scan_instances.export_scan(1, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/download&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">stream</span><span class="o">=</span><span class="kc">True</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
                <span class="s1">&#39;downloadType&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;export_format&#39;</span><span class="p">,</span> <span class="n">export_format</span><span class="p">,</span> <span class="nb">str</span><span class="p">,</span>
                    <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;scap1_2&#39;</span><span class="p">,</span> <span class="s1">&#39;v2&#39;</span><span class="p">],</span> <span class="n">default</span><span class="o">=</span><span class="s1">&#39;v2&#39;</span><span class="p">)})</span>

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

<div class="viewcode-block" id="ScanResultAPI.import_scan"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.import_scan">[docs]</a>    <span class="k">def</span> <span class="nf">import_scan</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fobj</span><span class="p">,</span> <span class="n">repo</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Imports a nessus file into Tenable.sc.</span>

<span class="sd">        :sc-api:`scan-result: import &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/import&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fobj (FileObject):</span>
<span class="sd">                The file-like object containing the Nessus file to import.</span>
<span class="sd">            repo (int):</span>
<span class="sd">                The repository id for the scan.</span>
<span class="sd">            auto_mitigation (int, optional):</span>
<span class="sd">                How many days to hold on to data before mitigating it?  The</span>
<span class="sd">                default value is 0.</span>
<span class="sd">            host_tracking (bool, optional):</span>
<span class="sd">                Should DHCP host tracking be enabled?  The default is False.</span>
<span class="sd">            vhosts (bool, optional):</span>
<span class="sd">                Should virtual host logic be enabled for the scan?  The default</span>
<span class="sd">                is ``False``.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty string response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; with open(&#39;example.nessus&#39;) as fobj:</span>
<span class="sd">            ...     sc.scan_instances.import_scan(fobj, 1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;repo&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">repo</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">scans</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="n">payload</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">fobj</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span>
            <span class="s1">&#39;scanResult/import&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.reimport_scan"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.reimport_scan">[docs]</a>    <span class="k">def</span> <span class="nf">reimport_scan</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Re-imports an existing scan into the cumulative repository.</span>

<span class="sd">        :sc-api:`scan-result: re-import &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/import&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int):</span>
<span class="sd">                The scan instance identifier.</span>
<span class="sd">            auto_mitigation (int, optional):</span>
<span class="sd">                How many days to hold on to data before mitigating it?  The</span>
<span class="sd">                default value is 0.</span>
<span class="sd">            host_tracking (bool, optional):</span>
<span class="sd">                Should DHCP host tracking be enabled?  The default is False.</span>
<span class="sd">            vhosts (bool, optional):</span>
<span class="sd">                Should virtual host logic be enabled for the scan?  The default</span>
<span class="sd">                is ``False``.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty string response.</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.reimport_scan(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">scans</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/import&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
            <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">start_time</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">end_time</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">optimize</span><span class="o">=</span><span class="kc">True</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of scan instances.</span>

<span class="sd">        :sc-api:`scan-result: list &lt;Scan-Result.html#ScanResultRESTReference-/scanResult&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">            start_time (int, optional):</span>
<span class="sd">                Epoch time to start search (searches against createdTime and defaults to now-30d)</span>
<span class="sd">            end_time (int, optional):</span>
<span class="sd">                Epoch time to end search (searches against createdTime and defaults to now)</span>
<span class="sd">            optimize (bool, optional):</span>
<span class="sd">                Informs Tenable.sc to optimize completed scan results.  If left</span>
<span class="sd">                unspecified, the default is `True`.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                A list of scan instance resources.</span>

<span class="sd">        Examples:</span>
<span class="sd">            * Retrieving all of the manageable scans instances:</span>

<span class="sd">            &gt;&gt;&gt; for scan in sc.scan_instances.list()[&#39;manageable&#39;]:</span>
<span class="sd">            ...     pprint(scan)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">(</span>
            <span class="n">optimizeCompletedScanResults</span><span class="o">=</span><span class="nb">str</span><span class="p">(</span><span class="n">optimize</span><span class="p">)</span><span class="o">.</span><span class="n">lower</span><span class="p">()</span>
        <span class="p">)</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>

        <span class="k">if</span> <span class="n">start_time</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;startTime&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;start_time&#39;</span><span class="p">,</span> <span class="n">start_time</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>

        <span class="k">if</span> <span class="n">end_time</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;endTime&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;end_time&#39;</span><span class="p">,</span> <span class="n">end_time</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>

        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;scanResult&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.pause"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.pause">[docs]</a>    <span class="k">def</span> <span class="nf">pause</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Pauses a running scan instance.  Note that this will not impact agent</span>
<span class="sd">        scan instances.</span>

<span class="sd">        &quot;sc-api:`scan-result: pause &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/pause&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the scan instance.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The Scan instance state</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.pause(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/pause&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
            <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.resume"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.resume">[docs]</a>    <span class="k">def</span> <span class="nf">resume</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Resumes a paused scan instance.  Note that this will not impact agent</span>
<span class="sd">        scan instances.</span>

<span class="sd">        :sc-api:`scan-result: resume &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/resume&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the scan instance.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The Scan instance state</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.resume(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/resume&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
            <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="ScanResultAPI.stop"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.scan_instances.ScanResultAPI.stop">[docs]</a>    <span class="k">def</span> <span class="nf">stop</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Stops a running scan instance.  Note that this will not impact agent</span>
<span class="sd">        scan instances.</span>

<span class="sd">        :sc-api:`scan-result: stop &lt;Scan-Result.html#ScanResultRESTReference-/scanResult/{id}/stop&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            id (int): The unique identifier for the scan instance.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The Scan instance state</span>

<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.scan_instances.stop(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;scanResult/</span><span class="si">{}</span><span class="s1">/stop&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
            <span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.scan_instances</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
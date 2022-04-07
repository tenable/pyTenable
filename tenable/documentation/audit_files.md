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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.audit_files</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.sc.audit_files</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Audit Files</span>
<span class="sd">===========</span>
<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`Audit File &lt;AuditFile.html&gt;` API and the</span>
<span class="sd">:sc-api:`Audit File Template &lt;AuditFile-Template.html&gt;` API.  These items are</span>
<span class="sd">typically seen under the **Scans: Audit Files** section of Tenable.sc.</span>
<span class="sd">Methods available on ``sc.audit_files``:</span>
<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: AuditFileAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>
<span class="kn">from</span> <span class="nn">io</span> <span class="kn">import</span> <span class="n">BytesIO</span>
<span class="kn">from</span> <span class="nn">os.path</span> <span class="kn">import</span> <span class="n">basename</span>
<div class="viewcode-block" id="AuditFileAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI">[docs]</a><span class="k">class</span> <span class="nc">AuditFileAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_constructor</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Handles parsing the keywords and returns a audit file definition document</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">if</span> <span class="s1">&#39;name&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the name parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;name&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;description&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the description parameter is a string,</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;description&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;description&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;type&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the type is one of the 3 possible audit file types:</span>
            <span class="c1"># &quot;&quot;, &quot;scapWindows&quot;, or &quot;scapLinux&quot;.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;type&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;type&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;&#39;</span><span class="p">,</span> <span class="s1">&#39;scapWindows&#39;</span><span class="p">,</span> <span class="s1">&#39;scapLinux&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;template&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Convert the template parameter into the auditFileTemplate</span>
            <span class="c1"># sub-document and verify that the input is an integer value.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;auditFileTemplate&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;id&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;template&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">],</span> <span class="nb">int</span><span class="p">)}</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;template&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;vars&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># expand the the vars dict into a series of key/value documents.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;variables&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="p">[{</span>
                    <span class="s1">&#39;name&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;var:name&#39;</span><span class="p">,</span> <span class="n">k</span><span class="p">,</span> <span class="nb">str</span><span class="p">),</span>
                    <span class="s1">&#39;value&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;var:value&#39;</span><span class="p">,</span> <span class="n">v</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="p">}</span> <span class="k">for</span> <span class="n">k</span><span class="p">,</span><span class="n">v</span> <span class="ow">in</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;vars&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vars&#39;</span><span class="p">],</span> <span class="nb">dict</span><span class="p">)</span><span class="o">.</span><span class="n">items</span><span class="p">()]</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;vars&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;filename&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the filename parameter is a string.</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filename&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="s1">&#39;orig_filename&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># validate the the original_filename parameter is of type string and</span>
            <span class="c1"># then store it in the CamelCase equiv:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;originalFilename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;orig_filename&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orig_filename&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orig_filename&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;version&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the version parameter is of type string and falls</span>
            <span class="c1"># within the expected range of values</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;version&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;version&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">,</span>
                <span class="n">choices</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;1.0&#39;</span><span class="p">,</span> <span class="s1">&#39;1.1&#39;</span><span class="p">,</span> <span class="s1">&#39;1.2&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;benchmark&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the benchmark name is a string and then store it</span>
            <span class="c1"># in the benchmarkName attribute.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;benchmarkName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;benchmark&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;benchmark&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;benchmark&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;profile&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the profile name is a string and then store it in</span>
            <span class="c1"># the profileName attribute.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;profileName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;profile&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;profile&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;profile&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;data_stream&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="c1"># Validate that the profile_stream attribute is a string and then</span>
            <span class="c1"># store it in the dataStreamName attribute.</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;dataStreamName&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;data_stream&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_stream&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;data_stream&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;tailoring_filename&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoringFilename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;tailoring_filename&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_filename&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_filename&#39;</span><span class="p">])</span>
        <span class="k">if</span> <span class="s1">&#39;tailoring_orig_filename&#39;</span> <span class="ow">in</span> <span class="n">kw</span><span class="p">:</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoringOriginalFilename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span>
                <span class="s1">&#39;tailoring_orig_filename&#39;</span><span class="p">,</span> <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_orig_filename&#39;</span><span class="p">],</span> <span class="nb">str</span><span class="p">)</span>
            <span class="k">del</span><span class="p">(</span><span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_orig_filename&#39;</span><span class="p">])</span>
        <span class="k">return</span> <span class="n">kw</span>
<div class="viewcode-block" id="AuditFileAPI.create"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.create">[docs]</a>    <span class="k">def</span> <span class="nf">create</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">name</span><span class="p">,</span> <span class="n">audit_file</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">tailoring_file</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Creates a audit file.</span>
<span class="sd">        :sc-api:`audit file: create &lt;AuditFile.html#auditFile_POST&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            name (str):</span>
<span class="sd">                The name of the audit file.</span>
<span class="sd">            audit_file (FileObject, optional):</span>
<span class="sd">                The file-like object containing the audit file if uploading a</span>
<span class="sd">                custom audit file.</span>
<span class="sd">            benchmark (str, optional):</span>
<span class="sd">                When the type is set to either SCAP datatype, this specifies the</span>
<span class="sd">                name of the benchmark.</span>
<span class="sd">            data_stream (str, optional):</span>
<span class="sd">                When using version 1.2 of either SCAP datatype, you must specify</span>
<span class="sd">                the name of the data stream.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description of for the audit file.</span>
<span class="sd">            profile (str, optional):</span>
<span class="sd">                When the type is set to either SCAP datatype, this specifies the</span>
<span class="sd">                name of the profile.</span>
<span class="sd">            tailoring_file (FileObject, optional):</span>
<span class="sd">                When the SCAP version is set to 1.2, this tailoring file can</span>
<span class="sd">                optionally be provided.</span>
<span class="sd">            template (int, optional):</span>
<span class="sd">                The audit file template it to use.  If using a template, then no</span>
<span class="sd">                file is uploaded.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of audit file to upload.  Generally only used when</span>
<span class="sd">                uploading SCAP content as it will default to the Tenable-created</span>
<span class="sd">                audit-file format.  Supported SCAP values are ``scapWindows``</span>
<span class="sd">                and ``scapLinux``.</span>
<span class="sd">            vars (dict, optional):</span>
<span class="sd">                If a template is specified, then this dictionary specifies the</span>
<span class="sd">                parameters within the template to customize and what those</span>
<span class="sd">                values should be.  The values are provided within the template</span>
<span class="sd">                definition.</span>
<span class="sd">            version (str, optional):</span>
<span class="sd">                When specifying a SCAP datatype, this informs Tenable.sc what</span>
<span class="sd">                version of SCAP this audit checklist is.  Supported values are</span>
<span class="sd">                ``1.0``, ``1.1``, and ``1.2``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly created audit file.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; audit = sc.audit_files.create()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;name&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">name</span>
        <span class="c1"># Upload and store the relevant information on the audit file that has</span>
        <span class="c1"># been provided.</span>
        <span class="k">if</span> <span class="n">audit_file</span><span class="p">:</span>
            <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">audit_file</span><span class="p">,</span> <span class="s1">&#39;name&#39;</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orig_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">basename</span><span class="p">(</span><span class="n">audit_file</span><span class="o">.</span><span class="n">name</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">audit_file</span><span class="p">)</span>
        <span class="c1"># Upload and store the relevant information on the tailoring file that</span>
        <span class="c1"># has been provided.</span>
        <span class="k">if</span> <span class="n">tailoring_file</span><span class="p">:</span>
            <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">tailoring_file</span><span class="p">,</span> <span class="s1">&#39;name&#39;</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_orig_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">basename</span><span class="p">(</span><span class="n">tailoring_file</span><span class="o">.</span><span class="n">name</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">tailoring_file</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;auditFile&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.details">[docs]</a>    <span class="k">def</span> <span class="nf">details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for a specific audit file.</span>
<span class="sd">        :sc-api:`audit file: details &lt;AuditFile.html#AuditFileRESTReference-/auditFile/{id}&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The identifier for the audit file.</span>
<span class="sd">            fields (list, optional): A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The audit file resource record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; audit = sc.audit_files.details(1)</span>
<span class="sd">            &gt;&gt;&gt; pprint(audit)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFile/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.edit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.edit">[docs]</a>    <span class="k">def</span> <span class="nf">edit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">audit_file</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">tailoring_file</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="o">**</span><span class="n">kw</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Edits a audit file.</span>
<span class="sd">        :sc-api:`audit file: edit &lt;AuditFile.html#auditFile_id_PATCH&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            audit_file (FileObject, optional):</span>
<span class="sd">                The file-like object containing the audit file if uploading a</span>
<span class="sd">                custom audit file.</span>
<span class="sd">            benchmark (str, optional):</span>
<span class="sd">                When the type is set to either SCAP datatype, this specifies the</span>
<span class="sd">                name of the benchmark.</span>
<span class="sd">            data_stream (str, optional):</span>
<span class="sd">                When using version 1.2 of either SCAP datatype, you must specify</span>
<span class="sd">                the name of the data stream.</span>
<span class="sd">            description (str, optional):</span>
<span class="sd">                A description of for the audit file.</span>
<span class="sd">            name (str, optional):</span>
<span class="sd">                The name of the audit file.</span>
<span class="sd">            profile (str, optional):</span>
<span class="sd">                When the type is set to either SCAP datatype, this specifies the</span>
<span class="sd">                name of the profile.</span>
<span class="sd">            tailoring_file (FileObject, optional):</span>
<span class="sd">                When the SCAP version is set to 1.2, this tailoring file can</span>
<span class="sd">                optionally be provided.</span>
<span class="sd">            template (int, optional):</span>
<span class="sd">                The audit file template it to use.  If using a template, then no</span>
<span class="sd">                file is uploaded.</span>
<span class="sd">            type (str, optional):</span>
<span class="sd">                The type of audit file to upload.  Generally only used when</span>
<span class="sd">                uploading SCAP content as it will default to the Tenable-created</span>
<span class="sd">                audit-file format.  Supported SCAP values are ``scapWindows``</span>
<span class="sd">                and ``scapLinux``.</span>
<span class="sd">            vars (dict, optional):</span>
<span class="sd">                If a template is specified, then this dictionary specifies the</span>
<span class="sd">                parameters within the template to customize and what those</span>
<span class="sd">                values should be.  The values are provided within the template</span>
<span class="sd">                definition.</span>
<span class="sd">            version (str, optional):</span>
<span class="sd">                When specifying a SCAP datatype, this informs Tenable.sc what</span>
<span class="sd">                version of SCAP this audit checklist is.  Supported values are</span>
<span class="sd">                ``1.0``, ``1.1``, and ``1.2``.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The newly updated audit file.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; audit = sc.audit_files.edit()</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># Upload and store the relevant information on the audit file that has</span>
        <span class="c1"># been provided.</span>
        <span class="k">if</span> <span class="n">audit_file</span><span class="p">:</span>
            <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">audit_file</span><span class="p">,</span> <span class="s1">&#39;name&#39;</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;orig_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">basename</span><span class="p">(</span><span class="n">audit_file</span><span class="o">.</span><span class="n">name</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">audit_file</span><span class="p">)</span>
        <span class="c1"># Upload and store the relevant information on the tailoring file that</span>
        <span class="c1"># has been provided.</span>
        <span class="k">if</span> <span class="n">tailoring_file</span><span class="p">:</span>
            <span class="k">if</span> <span class="nb">hasattr</span><span class="p">(</span><span class="n">tailoring_file</span><span class="p">,</span> <span class="s1">&#39;name&#39;</span><span class="p">):</span>
                <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_orig_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="n">basename</span><span class="p">(</span><span class="n">tailoring_file</span><span class="o">.</span><span class="n">name</span><span class="p">)</span>
            <span class="n">kw</span><span class="p">[</span><span class="s1">&#39;tailoring_filename&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">files</span><span class="o">.</span><span class="n">upload</span><span class="p">(</span><span class="n">tailoring_file</span><span class="p">)</span>
        <span class="n">payload</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_constructor</span><span class="p">(</span><span class="o">**</span><span class="n">kw</span><span class="p">)</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">patch</span><span class="p">(</span><span class="s1">&#39;auditFile/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">json</span><span class="o">=</span><span class="n">payload</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.delete"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.delete">[docs]</a>    <span class="k">def</span> <span class="nf">delete</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes a audit file.</span>
<span class="sd">        :sc-api:`audit file: delete &lt;AuditFile.html#auditFile_id_DELETE&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The numeric identifier for the audit file to remove.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                An empty response.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; sc.audit_files.delete(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">delete</span><span class="p">(</span><span class="s1">&#39;auditFile/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)))</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.list">[docs]</a>    <span class="k">def</span> <span class="nf">list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Retrieves the list of audit file definitions.</span>
<span class="sd">        :sc-api:`audit file: list &lt;AuditFile.html#AuditFileRESTReference-/auditFile&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return for each audit file.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                A list of audit file resources.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for audit in sc.audit_files.list():</span>
<span class="sd">            ...     pprint(audit)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFile&#39;</span><span class="p">,</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.export_audit"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.export_audit">[docs]</a>    <span class="k">def</span> <span class="nf">export_audit</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fobj</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Exports an Audit File.</span>
<span class="sd">        :sc-api:`audit file: export &lt;AuditFile.html#AuditFileRESTReference-/auditFile/{id}/export&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int): The audit file numeric identifier.</span>
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
<span class="sd">            ...     sc.audit_files.export_audit(1, fobj)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">resp</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFile/</span><span class="si">{}</span><span class="s1">/export&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
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
<div class="viewcode-block" id="AuditFileAPI.template_categories"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.template_categories">[docs]</a>    <span class="k">def</span> <span class="nf">template_categories</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the audit file template categories</span>
<span class="sd">        :sc-api:`audit template: categories &lt;AuditFile-Template.html#auditFileTemplate_categories_GET&gt;`</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of audit file category listing dicts.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for cat in sc.audit_files.template_categorties():</span>
<span class="sd">            ...     pprint(cat)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFileTemplate/categories&#39;</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.template_details"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.template_details">[docs]</a>    <span class="k">def</span> <span class="nf">template_details</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the details for the specified audit file template id.</span>
<span class="sd">        :sc-api:`audit template: details &lt;AuditFile-Template.html#auditFileTemplate_id_GET&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            id (int):</span>
<span class="sd">                The numeric identifier for the audit file template.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`dict`:</span>
<span class="sd">                The audit file template record.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; tmpl = sc.audit_files.template_details(1)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFileTemplate/</span><span class="si">{}</span><span class="s1">&#39;</span><span class="o">.</span><span class="n">format</span><span class="p">(</span>
            <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;id&#39;</span><span class="p">,</span> <span class="nb">id</span><span class="p">,</span> <span class="nb">int</span><span class="p">)),</span> <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div>
<div class="viewcode-block" id="AuditFileAPI.template_list"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.audit_files.AuditFileAPI.template_list">[docs]</a>    <span class="k">def</span> <span class="nf">template_list</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">category</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">search</span><span class="o">=</span><span class="kc">None</span><span class="p">,</span> <span class="n">fields</span><span class="o">=</span><span class="kc">None</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Returns the list of audit file templates.</span>
<span class="sd">        :sc-api:`audit templates: list &lt;AuditFile-Template.html#AuditFileTemplateRESTReference-/auditFileTemplate&gt;`</span>
<span class="sd">        Args:</span>
<span class="sd">            category (int, optional):</span>
<span class="sd">                Restrict the results to only the specified category id.</span>
<span class="sd">            fields (list, optional):</span>
<span class="sd">                A list of attributes to return.</span>
<span class="sd">            search (str, optional):</span>
<span class="sd">                Restrict the response to only audit file names that match the</span>
<span class="sd">                search string specified.</span>
<span class="sd">        Returns:</span>
<span class="sd">            :obj:`list`:</span>
<span class="sd">                List of audit file records.</span>
<span class="sd">        Examples:</span>
<span class="sd">            &gt;&gt;&gt; for tmpl in sc.audit_files.template_list():</span>
<span class="sd">            ...     pprint(tmpl)</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="n">params</span> <span class="o">=</span> <span class="nb">dict</span><span class="p">()</span>
        <span class="k">if</span> <span class="n">category</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;categoryID&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;category&#39;</span><span class="p">,</span> <span class="n">category</span><span class="p">,</span> <span class="nb">int</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">search</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;searchString&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;search&#39;</span><span class="p">,</span> <span class="n">search</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">fields</span><span class="p">:</span>
            <span class="n">params</span><span class="p">[</span><span class="s1">&#39;fields&#39;</span><span class="p">]</span> <span class="o">=</span> <span class="s1">&#39;,&#39;</span><span class="o">.</span><span class="n">join</span><span class="p">([</span><span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;field&#39;</span><span class="p">,</span> <span class="n">f</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
                <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">fields</span><span class="p">])</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">get</span><span class="p">(</span><span class="s1">&#39;auditFileTemplate&#39;</span><span class="p">,</span>
            <span class="n">params</span><span class="o">=</span><span class="n">params</span><span class="p">)</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.audit_files</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
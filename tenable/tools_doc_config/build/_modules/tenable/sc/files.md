
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.sc.files &#8212; pyTenable  documentation</title>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.files</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.sc.files</h1><div class="highlight"><pre>
<span></span><span class="sd">&#39;&#39;&#39;</span>
<span class="sd">Files</span>
<span class="sd">=====</span>

<span class="sd">The following methods allow for interaction into the Tenable.sc</span>
<span class="sd">:sc-api:`File &lt;File.html&gt;` API.</span>

<span class="sd">Methods available on ``sc.files``:</span>

<span class="sd">.. rst-class:: hide-signature</span>
<span class="sd">.. autoclass:: FileAPI</span>
<span class="sd">    :members:</span>
<span class="sd">&#39;&#39;&#39;</span>
<span class="kn">from</span> <span class="nn">.base</span> <span class="kn">import</span> <span class="n">SCEndpoint</span>

<div class="viewcode-block" id="FileAPI"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.files.FileAPI">[docs]</a><span class="k">class</span> <span class="nc">FileAPI</span><span class="p">(</span><span class="n">SCEndpoint</span><span class="p">):</span>
<div class="viewcode-block" id="FileAPI.upload"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.files.FileAPI.upload">[docs]</a>    <span class="k">def</span> <span class="nf">upload</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">fobj</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Uploads a file into SecurityCenter and returns the file identifier</span>
<span class="sd">        to be used for subsequent calls.</span>

<span class="sd">        :sc-api:`file: upload &lt;File.html#FileRESTReference-/file/upload&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            fobj (FileObj): The file object to upload into SecurityCenter.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                The filename identifier to use for subsequent calls in</span>
<span class="sd">                Tenable.sc.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;file/upload&#39;</span><span class="p">,</span> <span class="n">files</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;Filedata&#39;</span><span class="p">:</span> <span class="n">fobj</span><span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span></div>

<div class="viewcode-block" id="FileAPI.clear"><a class="viewcode-back" href="../../../tenable.sc.md#tenable.sc.files.FileAPI.clear">[docs]</a>    <span class="k">def</span> <span class="nf">clear</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">filename</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        Removes the requested file from Tenable.sc.</span>

<span class="sd">        :sc-api:`file: clear &lt;File.html#FileRESTReference-/file/clear&gt;`</span>

<span class="sd">        Args:</span>
<span class="sd">            filename (str): The file identifier associated to the file.</span>

<span class="sd">        Returns:</span>
<span class="sd">            :obj:`str`:</span>
<span class="sd">                The file location on disk that was removed.</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="k">return</span> <span class="bp">self</span><span class="o">.</span><span class="n">_api</span><span class="o">.</span><span class="n">post</span><span class="p">(</span><span class="s1">&#39;file/clear&#39;</span><span class="p">,</span> <span class="n">json</span><span class="o">=</span><span class="p">{</span>
            <span class="s1">&#39;filename&#39;</span><span class="p">:</span> <span class="bp">self</span><span class="o">.</span><span class="n">_check</span><span class="p">(</span><span class="s1">&#39;filename&#39;</span><span class="p">,</span> <span class="n">filename</span><span class="p">,</span> <span class="nb">str</span><span class="p">)</span>
        <span class="p">})</span><span class="o">.</span><span class="n">json</span><span class="p">()[</span><span class="s1">&#39;response&#39;</span><span class="p">][</span><span class="s1">&#39;filename&#39;</span><span class="p">]</span></div></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.sc.files</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
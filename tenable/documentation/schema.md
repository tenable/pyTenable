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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.base.schema</a></li> 
      </ul>
    </div>  
    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
  <h1>Source code for tenable.ad.base.schema</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">typing</span> <span class="kn">import</span> <span class="n">Optional</span><span class="p">,</span> <span class="n">List</span>
<span class="kn">from</span> <span class="nn">marshmallow</span> <span class="kn">import</span> <span class="n">Schema</span><span class="p">,</span> <span class="n">fields</span><span class="p">,</span> <span class="n">ValidationError</span>
<div class="viewcode-block" id="camelcase"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.camelcase">[docs]</a><span class="k">def</span> <span class="nf">camelcase</span><span class="p">(</span><span class="n">s</span><span class="p">):</span>
    <span class="n">parts</span> <span class="o">=</span> <span class="nb">iter</span><span class="p">(</span><span class="n">s</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s2">&quot;_&quot;</span><span class="p">))</span>
    <span class="k">return</span> <span class="nb">next</span><span class="p">(</span><span class="n">parts</span><span class="p">)</span> <span class="o">+</span> <span class="s2">&quot;&quot;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">i</span><span class="o">.</span><span class="n">title</span><span class="p">()</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">parts</span><span class="p">)</span></div>
<div class="viewcode-block" id="last_word_uppercase"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.last_word_uppercase">[docs]</a><span class="k">def</span> <span class="nf">last_word_uppercase</span><span class="p">(</span><span class="n">s</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    converts last word to uppercase</span>
<span class="sd">    Example:</span>
<span class="sd">        example_field -&gt; exampleFIELD</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="n">parts</span> <span class="o">=</span> <span class="n">s</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s2">&quot;_&quot;</span><span class="p">)</span>
    <span class="k">return</span> <span class="n">parts</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">+</span> <span class="s2">&quot;&quot;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">i</span><span class="o">.</span><span class="n">title</span><span class="p">()</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">parts</span><span class="p">[</span><span class="mi">1</span><span class="p">:</span><span class="nb">len</span><span class="p">(</span><span class="n">parts</span><span class="p">)</span> <span class="o">-</span> <span class="mi">1</span><span class="p">])</span> <span class="o">+</span> \
           <span class="n">parts</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">upper</span><span class="p">()</span></div>
<div class="viewcode-block" id="convert_keys_to_camel"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.convert_keys_to_camel">[docs]</a><span class="k">def</span> <span class="nf">convert_keys_to_camel</span><span class="p">(</span><span class="n">data</span><span class="p">:</span> <span class="nb">dict</span><span class="p">,</span>
                          <span class="n">special</span><span class="p">:</span> <span class="n">Optional</span><span class="p">[</span><span class="n">List</span><span class="p">[</span><span class="nb">str</span><span class="p">]]</span> <span class="o">=</span> <span class="kc">None</span>
                          <span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">dict</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    Convert dictionary keys to camel case</span>
<span class="sd">    Example:</span>
<span class="sd">        example_field -&gt; exampleField</span>
<span class="sd">    and for special field names</span>
<span class="sd">    will convert last word to uppercase.</span>
<span class="sd">    Example:</span>
<span class="sd">        example_field -&gt; exampleFIELD</span>
<span class="sd">    Args:</span>
<span class="sd">        data (dict):</span>
<span class="sd">            The data dictionary.</span>
<span class="sd">        special (optional, list[str]):</span>
<span class="sd">            The list of special field for converting last word to uppercase.</span>
<span class="sd">    &#39;&#39;&#39;</span>
    <span class="k">if</span> <span class="n">special</span> <span class="ow">is</span> <span class="kc">None</span><span class="p">:</span>
        <span class="n">special</span> <span class="o">=</span> <span class="p">[]</span>
    <span class="n">resp</span> <span class="o">=</span> <span class="p">{}</span>
    <span class="k">for</span> <span class="n">key</span><span class="p">,</span> <span class="n">value</span> <span class="ow">in</span> <span class="n">data</span><span class="o">.</span><span class="n">items</span><span class="p">():</span>
        <span class="k">if</span> <span class="n">key</span> <span class="ow">in</span> <span class="n">special</span><span class="p">:</span>
            <span class="n">resp</span><span class="p">[</span><span class="n">last_word_uppercase</span><span class="p">(</span><span class="n">key</span><span class="p">)]</span> <span class="o">=</span> <span class="n">value</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">resp</span><span class="p">[</span><span class="n">camelcase</span><span class="p">(</span><span class="n">key</span><span class="p">)]</span> <span class="o">=</span> <span class="n">value</span>
    <span class="k">return</span> <span class="n">resp</span></div>
<div class="viewcode-block" id="CamelCaseSchema"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema">[docs]</a><span class="k">class</span> <span class="nc">CamelCaseSchema</span><span class="p">(</span><span class="n">Schema</span><span class="p">):</span>
    <span class="sd">&quot;&quot;&quot;Schema that uses camel-case for its external representation</span>
<span class="sd">    and snake-case for its internal representation.</span>
<span class="sd">    &quot;&quot;&quot;</span>
<div class="viewcode-block" id="CamelCaseSchema.on_bind_field"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.CamelCaseSchema.on_bind_field">[docs]</a>    <span class="k">def</span> <span class="nf">on_bind_field</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">field_name</span><span class="p">,</span> <span class="n">field_obj</span><span class="p">):</span>
        <span class="n">last_word_uppercase_field_names</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;search_user_dn&#39;</span><span class="p">]</span>
        <span class="k">if</span> <span class="n">field_name</span> <span class="ow">in</span> <span class="n">last_word_uppercase_field_names</span><span class="p">:</span>
            <span class="n">field_obj</span><span class="o">.</span><span class="n">data_key</span> <span class="o">=</span> <span class="n">last_word_uppercase</span><span class="p">(</span>
                <span class="n">field_obj</span><span class="o">.</span><span class="n">data_key</span> <span class="ow">or</span> <span class="n">field_name</span><span class="p">)</span>
        <span class="k">else</span><span class="p">:</span>
            <span class="n">field_obj</span><span class="o">.</span><span class="n">data_key</span> <span class="o">=</span> <span class="n">camelcase</span><span class="p">(</span><span class="n">field_obj</span><span class="o">.</span><span class="n">data_key</span> <span class="ow">or</span> <span class="n">field_name</span><span class="p">)</span></div></div>
<div class="viewcode-block" id="BoolInt"><a class="viewcode-back" href="../../../../tenable.ad.base.md#tenable.ad.base.schema.BoolInt">[docs]</a><span class="k">class</span> <span class="nc">BoolInt</span><span class="p">(</span><span class="n">fields</span><span class="o">.</span><span class="n">Boolean</span><span class="p">):</span>
    <span class="sd">&#39;&#39;&#39;Schema to return an integer value for given boolean value&#39;&#39;&#39;</span>
    <span class="k">def</span> <span class="nf">_serialize</span><span class="p">(</span><span class="bp">self</span><span class="p">,</span> <span class="n">value</span><span class="p">,</span> <span class="n">attr</span><span class="p">,</span> <span class="n">obj</span><span class="p">,</span> <span class="o">**</span><span class="n">kwargs</span><span class="p">)</span> <span class="o">-&gt;</span> <span class="nb">int</span><span class="p">:</span>
        <span class="k">return</span> <span class="nb">int</span><span class="p">(</span><span class="n">value</span><span class="p">)</span> <span class="k">if</span> <span class="n">value</span> <span class="k">else</span> <span class="mi">0</span></div>
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
        <li class="nav-item nav-item-this"><a href="">tenable.ad.base.schema</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
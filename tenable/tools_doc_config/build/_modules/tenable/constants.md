
<!DOCTYPE html>

<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>tenable.constants &#8212; pyTenable  documentation</title>
    <link rel="stylesheet" type="text/css" href="../../_static/pygments.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/classic.css" />
    <link rel="stylesheet" type="text/css" href="../../_static/custom.css" />
    
    <script data-url_root="../../" id="documentation_options" src="../../_static/documentation_options.js"></script>
    <script src="../../_static/jquery.js"></script>
    <script src="../../_static/underscore.js"></script>
    <script src="../../_static/doctools.js"></script>
    
    <link rel="index" title="Index" href="../../genindex.md" />
    <link rel="search" title="Search" href="../../search.md" /> 
  </head><body>
    <div class="related" role="navigation" aria-label="related navigation">
      <h3>Navigation</h3>
      <ul>
        <li class="right" style="margin-right: 10px">
          <a href="../../genindex.md" title="General Index"
             accesskey="I">index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" accesskey="U">Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.constants</a></li> 
      </ul>
    </div>  

    <div class="document">
      <div class="documentwrapper">
          <div class="body" role="main">
            
  <h1>Source code for tenable.constants</h1><div class="highlight"><pre>
<span></span><span class="kn">from</span> <span class="nn">datetime</span> <span class="kn">import</span> <span class="n">datetime</span><span class="p">,</span> <span class="n">timedelta</span>


<div class="viewcode-block" id="IOConstants"><a class="viewcode-back" href="../../README.md#tenable.constants.IOConstants">[docs]</a><span class="k">class</span> <span class="nc">IOConstants</span><span class="p">:</span>
    <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">    This class contains all the constants related to IO package</span>
<span class="sd">    &#39;&#39;&#39;</span>

<div class="viewcode-block" id="IOConstants.CaseConst"><a class="viewcode-back" href="../../README.md#tenable.constants.IOConstants.CaseConst">[docs]</a>    <span class="k">class</span> <span class="nc">CaseConst</span><span class="p">:</span>
        <span class="c1"># for case parameter in check</span>
        <span class="n">uppercase</span> <span class="o">=</span> <span class="s1">&#39;upper&#39;</span>
        <span class="n">lowecase</span> <span class="o">=</span> <span class="s1">&#39;lower&#39;</span></div>

<div class="viewcode-block" id="IOConstants.ScheduleConst"><a class="viewcode-back" href="../../README.md#tenable.constants.IOConstants.ScheduleConst">[docs]</a>    <span class="k">class</span> <span class="nc">ScheduleConst</span><span class="p">:</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        This class contains common constants required for schedule</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># frequency type</span>
        <span class="n">onetime</span> <span class="o">=</span> <span class="s1">&#39;ONETIME&#39;</span>
        <span class="n">daily</span> <span class="o">=</span> <span class="s1">&#39;DAILY&#39;</span>
        <span class="n">weekly</span> <span class="o">=</span> <span class="s1">&#39;WEEKLY&#39;</span>
        <span class="n">monthly</span> <span class="o">=</span> <span class="s1">&#39;MONTHLY&#39;</span>
        <span class="n">yearly</span> <span class="o">=</span> <span class="s1">&#39;YEARLY&#39;</span>

        <span class="c1"># frequency</span>
        <span class="n">frequency</span> <span class="o">=</span> <span class="s1">&#39;frequency&#39;</span>
        <span class="n">frequency_default</span> <span class="o">=</span> <span class="n">onetime</span>
        <span class="n">frequency_choice</span> <span class="o">=</span> <span class="p">[</span><span class="n">onetime</span><span class="p">,</span> <span class="n">daily</span><span class="p">,</span> <span class="n">weekly</span><span class="p">,</span> <span class="n">monthly</span><span class="p">,</span> <span class="n">yearly</span><span class="p">]</span>

        <span class="c1"># frequency-WEEKLY</span>
        <span class="n">weekdays</span> <span class="o">=</span> <span class="s1">&#39;byweekday&#39;</span>
        <span class="n">weekdays_default</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;SU&#39;</span><span class="p">,</span> <span class="s1">&#39;MO&#39;</span><span class="p">,</span> <span class="s1">&#39;TU&#39;</span><span class="p">,</span> <span class="s1">&#39;WE&#39;</span><span class="p">,</span> <span class="s1">&#39;TH&#39;</span><span class="p">,</span> <span class="s1">&#39;FR&#39;</span><span class="p">,</span> <span class="s1">&#39;SA&#39;</span><span class="p">]</span>

        <span class="c1"># frequency-MONTHLY</span>
        <span class="n">day_of_month</span> <span class="o">=</span> <span class="s1">&#39;day_of_month&#39;</span>
        <span class="n">day_of_month_choice</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="mi">32</span><span class="p">))</span>
        <span class="n">day_of_month_default</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">today</span><span class="p">()</span><span class="o">.</span><span class="n">day</span>

        <span class="c1"># INTERVAL</span>
        <span class="n">interval</span> <span class="o">=</span> <span class="s1">&#39;interval&#39;</span>
        <span class="n">interval_default</span> <span class="o">=</span> <span class="mi">1</span>

        <span class="c1"># START-TIME</span>
        <span class="n">start_time</span> <span class="o">=</span> <span class="s1">&#39;starttime&#39;</span>
        <span class="n">start_time_default</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">utcnow</span><span class="p">()</span>

        <span class="c1"># END-TIME</span>
        <span class="n">end_time</span> <span class="o">=</span> <span class="s1">&#39;endtime&#39;</span>
        <span class="n">end_time_default</span> <span class="o">=</span> <span class="n">datetime</span><span class="o">.</span><span class="n">utcnow</span><span class="p">()</span> <span class="o">+</span> <span class="n">timedelta</span><span class="p">(</span><span class="n">hours</span><span class="o">=</span><span class="mi">1</span><span class="p">)</span>

        <span class="c1"># TIMEZONE</span>
        <span class="n">timezone</span> <span class="o">=</span> <span class="s1">&#39;timezone&#39;</span>
        <span class="n">timezone_default</span> <span class="o">=</span> <span class="s1">&#39;Etc/UTC&#39;</span>

        <span class="c1"># rrule</span>
        <span class="n">rrules</span> <span class="o">=</span> <span class="s1">&#39;rrules&#39;</span></div>

<div class="viewcode-block" id="IOConstants.ScanScheduleConst"><a class="viewcode-back" href="../../README.md#tenable.constants.IOConstants.ScanScheduleConst">[docs]</a>    <span class="k">class</span> <span class="nc">ScanScheduleConst</span><span class="p">(</span><span class="n">ScheduleConst</span><span class="p">):</span>
        <span class="sd">&#39;&#39;&#39;</span>
<span class="sd">        This class inherits all variables from ScheduleConst and</span>
<span class="sd">        contains additional variables required for scan scheduling</span>
<span class="sd">        &#39;&#39;&#39;</span>
        <span class="c1"># formatting and comparison values required in scan schedule</span>
        <span class="n">ffrequency</span> <span class="o">=</span> <span class="s1">&#39;FREQ=</span><span class="si">{}</span><span class="s1">&#39;</span>
        <span class="n">finterval</span> <span class="o">=</span> <span class="s1">&#39;INTERVAL=</span><span class="si">{}</span><span class="s1">&#39;</span>
        <span class="n">fbyweekday</span> <span class="o">=</span> <span class="s1">&#39;BYDAY=</span><span class="si">{}</span><span class="s1">&#39;</span>
        <span class="n">fbymonthday</span> <span class="o">=</span> <span class="s1">&#39;BYMONTHDAY=</span><span class="si">{}</span><span class="s1">&#39;</span>

        <span class="n">weekly_frequency</span> <span class="o">=</span> <span class="s1">&#39;FREQ=WEEKLY&#39;</span>
        <span class="n">monthly_frequency</span> <span class="o">=</span> <span class="s1">&#39;FREQ=MONTHLY&#39;</span>

        <span class="n">enabled</span> <span class="o">=</span> <span class="s1">&#39;enabled&#39;</span>
        <span class="n">launch</span> <span class="o">=</span> <span class="s1">&#39;launch&#39;</span>
        <span class="n">schedule_scan</span> <span class="o">=</span> <span class="s1">&#39;scheduleScan&#39;</span>

        <span class="c1"># start_time and end_time format used for converting datetime to and from format required for API</span>
        <span class="n">time_format</span> <span class="o">=</span> <span class="s1">&#39;%Y%m</span><span class="si">%d</span><span class="s1">T%H%M%S&#39;</span></div></div>
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
          <a href="../../genindex.md" title="General Index"
             >index</a></li>
        <li class="right" >
          <a href="../../py-modindex.md" title="Python Module Index"
             >modules</a> |</li>
        <li class="nav-item nav-item-0"><a href="../../README.md">pyTenable  documentation</a> &#187;</li>
          <li class="nav-item nav-item-1"><a href="../index.md" >Module code</a> &#187;</li>
        <li class="nav-item nav-item-this"><a href="">tenable.constants</a></li> 
      </ul>
    </div>
    <div class="footer" role="contentinfo">
        &#169; Copyright 2022, Tenable, Inc..
    </div>
  </body>
</html>
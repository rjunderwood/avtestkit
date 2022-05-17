# path

  Path utilities.

## API

   - [.extname(path)](#extnamepath)
   - [.basename(path)](#basenamepath)
   - [.dirname(path)](#dirnamepath)
<a name=""></a>
 
<a name="extnamepath"></a>
### .extname(path)
should return the extension.

```js
p.extname('png').should.equal('');
p.extname('.png').should.equal('.png');
p.extname('foo.png').should.equal('.png');
p.extname('foo/bar/baz.png').should.equal('.png');
p.extname('foo/bar.bar.baz/raz.png').should.equal('.png');
```

<a name="basenamepath"></a>
### .basename(path)
should return the last path segment.

```js
p.basename('foo').should.equal('foo');
p.basename('foo/bar/baz').should.equal('baz');
p.basename('foo/bar/baz').should.equal('baz');
p.basename('foo/bar/baz.png').should.equal('baz.png');
```

<a name="dirnamepath"></a>
### .dirname(path)
should return the leading segments.

```js
p.dirname('').should.equal('.');
p.dirname('foo').should.equal('.');
p.dirname('foo/bar/baz').should.equal('foo/bar');
p.dirname('foo/bar/baz.png').should.equal('foo/bar');
```


## License 

(The MIT License)

Copyright (c) 2012 TJ Holowaychuk &lt;tj@vision-media.ca&gt;

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
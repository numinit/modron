#!/usr/bin/env ruby

#
# Usage: scraper.rb <bestiary files to scrape>
# Output: A single CSV file on stdout.
#

require 'csv'

puts '# This is a gnarly comment, followed by a blank line. Sorry.'
puts
puts 'id,tag,name,description,alignment,languages,num_languages,ac,hp,speed,challenge'
ARGV.each_with_index do |fname, id|
  base = File.basename(fname, File.extname(fname))
  tag_match = base.match %r{\A\d+-\d+-\d+-(.+)\z}
  tag = tag_match[1]

  f = File.read fname
  name_match = f.match %r{^title: "([^"]+)"$}
  name = name_match ? name_match[1] : nil
  description_match = f.match %r{---\s+\*\*([^\*]+)\*\*$}
  description = description_match ? description_match[1] : nil
  if description
    description, _, alignment = description.rpartition(', ')
  else
    alignment = nil
  end
  languages_match = f.match %r{^\*\*Languages\*\* (.+)$}
  languages = languages_match ? languages_match[1].strip : ''
  if languages == "\u2014"
    languages = nil
    num_languages = nil
  else
    num_languages = languages.split(/,\s*/).length
  end

  ac_match = f.match %r{^\*\*Armor Class\*\* (\d+)}
  ac = ac_match ? Integer(ac_match[1]) : nil
  hp_match = f.match %r{^\*\*Hit Points\*\* (.+)$}
  hp = hp_match ? hp_match[1] : nil
  speed_match = f.match %r{^\*\*Speed\*\* (\d+)}
  speed = speed_match ? Integer(speed_match[1]) : nil
  challenge_match = f.match %r{^\*\*Challenge\*\* (\d+)}
  challenge = challenge_match ? Integer(challenge_match[1]) : nil
  puts CSV.generate_line([id + 1, tag, name, description, alignment, languages, num_languages, ac, hp, speed, challenge])
end

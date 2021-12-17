var thresh,
  words,
  active_words,
  selected_word = "none",
  wordAxis,
  data,
  active_data,
  highlighted_data,
  global_neighbors = [],
  pc,
  hideAxis = true,
  inSearch = false,
  afterHighlight = false,
  dragEndFlag = true;

bias_words = {
  gender: {
    Female:
      "she, daughter, hers, her, mother, woman, girl, herself, female, sister, daughters, mothers, women, girls, sisters, aunt, aunts, niece, nieces",
    Male: "he, son, his, him, father, man, boy, himself, male, brother, sons, fathers, men, boys, males, brothers, uncle, uncles, nephew, nephews",
  },
  race: {
    White:
      "white, whites, White, Whites, Caucasian, caucasian, European, european, Anglo",
    Black: "black, blacks, Black, Blacks, African, african, Afro",
  },
  religion: {
    Islam:
      "allah, ramadan, turban, emir, salaam, sunni, koran, imam, sultan, prophet, veil, ayatollah, shiite, mosque, islam, sheik, muslim, muhammad",
    Christanity:
      "baptism, messiah, catholicism, resurrection, christianity, salvation, protestant, gospel, trinity, jesus, christ, christian, cross, catholic, church",
  },
  age: {
    Old: "ethel,bernice,gertrude,agnes,cecil,wilbert,mortimer,edgar",
    Young: "tiffany,michelle,cindy,kristy,brad,eric,joey,billy",
  },
  economic: {
    Poor: "poor, poorer, poorest, poverty, destitude, needy, impoverished, economical, inexpensive, ruined, cheap, penurious, underprivileged, penniless, valueless, penury, indigence, bankrupt, beggarly, moneyless, insolvent",
    Rich: "rich, richer, richest, affluence, advantaged, wealthy, costly, exorbitant, expensive, exquisite, extravagant, flush, invaluable, lavish, luxuriant, luxurious, luxury, moneyed, opulent, plush, precious, priceless, privileged, prosperous, classy",
  },
};

var last_selected_axis_name = null;
var current_embedding = null;
$(document).ready(function () {
  $.get("/getFileNames/", function (res) {
    current_embedding = $("#dropdown_embedding").val();
    $('#dropdown_target option[value="Profession"]').attr("selected", true);
    changeTarget("Profession");
  });
  $.get(
    "/get_csv/",
    {
      scaling: $("#scaling").val(),
      embedding: $("#dropdown_embedding").val(),
    },
    function (res) {
      initialize(res);
    }
  );
});

function initialize(res) {
  (hideAxis = true), (inSearch = false), (afterHighlight = false);
  word_clicked = "";
  $("#neighbors_list").empty();
  data = JSON.parse(res);
  words = data.map(function (d) {
    return { title: d.word };
  });
  $(".ui.search").search("refresh");
  $(".ui.search").search({
    source: words,
    onSelect: function (d) {
      onClick(d.title);
    },
  });
  populate_histogram_bias_type(data[0]);
  $("#spinner").removeClass("lds-hourglass");
  $(".container-fluid").show();
  pc = createParallelCoord(data);
  pc.on("brushend", function (d) {
    populate_neighbors(d);
    if (inSearch) {
      d3.selectAll([pc.canvas["highlight"]]).classed("faded", true);
      d3.selectAll([pc.canvas["brushed"]]).classed("faded", false);
      pc.canvas["brushed"].globalAlpha = 1;
    }
  });
  pc.on("brush", function (d) {
    addExtentLabels(pc.brushExtents());
  });
}

function populate_histogram_bias_type(row) {
  bias_types = ["ALL"];
  for (key in row) {
    if (key == "word" || key == "type") {
      continue;
    }
    bias_types.push(key);
  }
}

function addExtentLabels(extents) {
  d3.selectAll(".extentLabels").remove();
  ex = [];
  d3.keys(extents).forEach(function (k) {
    axis_extents = extents[k];
    axis_extents.forEach(function (d) {
      y0 = pc.dimensions()[k].yscale(d[0]);
      y1 = pc.dimensions()[k].yscale(d[1]) + 5;
      x = pc.position(k) - 18;
      ex.push({ x: x, y: y0, color: "black", word: d[0].toFixed(2) });
      ex.push({ x: x, y: y1, color: "black", word: d[1].toFixed(2) });
    });
  });
  addSVGLabels(ex, "extentLabels");
}

$("#dropdown_embedding").change(function (event) {
  console.log("Change dropdown menu - Word Embedding");
  console.log($("#dropdown_embedding").val());
});

function searchWords(word) {
  $.get("/search/" + word, {}, (res) => {
    highlightWords(word, res);
  });
}

function populate_neighbors(brushed_data) {
  $("#neighbors_list").empty();
  brushed_data.forEach(function (neighbor, i) {
    $("#neighbors_list").append(
      '<li class="list-group-item">' + neighbor["word"] + "</li>"
    );
  });
}

function populate_brushed_words() {
  brushed_data = pc.brushed();
  $("#neighbors_list").empty();
  tmp = "";
  brushed_data.forEach(function (neighbor, i) {
    tmp = tmp + '<li class="list-group-item">' + neighbor["word"] + "</li>";
  });
  setTimeout(function () {
    $("#neighbors_list").html(tmp);
  }, 100);
}
